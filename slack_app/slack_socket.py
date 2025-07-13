import re
import json
from config.env import env
from slack_bolt import App
from lib.rag import user_input
from lib.semantics import query_rl
from database.db import User, ChatHistory
from slack_sdk.errors import SlackApiError
from database.db_session import get_session
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_app.blocks import get_hello_block, get_response_block, get_response_block_with_actions, get_actions_block, get_feedback_block, get_loading_block

app = App(token=env.slack.SLACK_TOKEN)
handler = SocketModeHandler(app, env.slack.SLACK_SOCKET_TOKEN)

session = get_session()

@app.event("app_home_opened")
def handle_home_opened(payload, client):
    user_id = payload["user"]
    channel_id = payload["channel"]
    user_details = client.users_info(user=user_id)
    print(user_details)
    
    user = session.get(User, user_id)

    if not user:
        fname = user_details["user"]["profile"]["first_name"]
        lname = user_details["user"]["profile"]["last_name"]
        email = user_details["user"]["profile"]["email"]
        slack_username = user_details["user"]["name"]
        
        try:
            user = User(
                id=user_id,
                fname=fname,
                lname=lname,
                slack_username=slack_username,
                email=email
            )
            
            session.add(user)
            session.commit()
        except Exception as e:
            print(f"Error creating user: {e}")
            
        hello_block = get_hello_block(fname)
        client.chat_postMessage(
            channel=channel_id,
            text="Welcome to the Policy Chatbot!",
            blocks=hello_block
        )

@app.event("app_mention")
def handle_mention(payload, client):
    channel_id = payload["channel"]
    user_id = payload["user"]
    user_query = payload["text"]
    thread_ts = payload.get("thread_ts", "")
    
    if thread_ts:
        chats = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts
        )
        
        thread_chat = "\n--- User Query Above, Thread Chats Start below use this part to accurately support the user query ---\n"
        for chat in chats["messages"][-5:]:
            word = re.sub(r"<([^>]*)>", "", chat["text"]).strip()
            thread_chat += f"{word}\n"
            
        thread_chat += "--- Thread Chats End ---\n"
        user_query += thread_chat

    if user_query:
        query_type = query_rl(user_query)
        
        loader_activated = False
        if query_type.name != 'chitchat':
            loader_activated = True
            loading_blocks = get_loading_block()
            message = message = client.chat_postMessage(
                channel=channel_id,
                user=user_id,
                thread_ts = thread_ts,
                text="Loading...",
                blocks=loading_blocks
            )
            print(message)
            
        data = user_input(user_query, channel_id, user_id)
        quoted_response = "\n".join(f"> {line}" for line in data.response.splitlines())
        source_str = ", ".join(data.sources)

        response_block = get_response_block(quoted_response)
        feedback_blocks = []
        
        try:
            user_role = ChatHistory(
                channel_id=channel_id,
                user_id=payload["user"],
                role="user",
                content=user_query
            )
            
            assistant_role = ChatHistory(
                channel_id=channel_id,
                user_id=payload["user"],
                role="assistant",
                content=data.response,
                docs_reffered=source_str
            )
            
            session.add_all([user_role, assistant_role])
            session.commit()
        except Exception as e:
            print(f"Error saving chat history: {e}")
            
        if data.query_type != 'chitchat' and not data.is_followup:
            feedback_blocks = get_feedback_block(type=data.response_type)

        try:
            if loader_activated:
                client.chat_update(
                    channel=channel_id,
                    ts=message['ts'] if message else thread_ts,
                    blocks=response_block
                )
                
                print("Sending the feedback block")
                
                client.chat_postEphemeral(
                    channel=channel_id,
                    user=user_id,  
                    thread_ts=thread_ts, 
                    text="Please share your feedback", 
                    blocks=feedback_blocks  
                )
            else:
                client.chat_postMessage(
                    channel=channel_id,
                    user=user_id,
                    thread_ts=thread_ts,
                    text=data.response,
                    blocks=response_block
                )
        except SlackApiError as e:
            print("Error sending message: {}".format(e.response["error"]))

@app.event("message")
def handle_message(payload, client):
    channel_id = payload["channel"]
    user_id = payload["user"]
    user_query = payload["text"]

    if user_query:
        loader_activated = False
        query_type = query_rl(user_query)
        
        if query_type.name != 'chitchat':
            loader_activated = True
            loading_blocks = get_loading_block()
            message = client.chat_postMessage(
                channel=channel_id,
                user=user_id,
                text="Loading...",
                blocks=loading_blocks
            )
        
        data = user_input(user_query, channel_id, user_id)
        quoted_response = "\n".join(f"> {line}" for line in data.response.splitlines())
        source_str = ", ".join(data.sources)
        
        try:
            user_role = ChatHistory(
                channel_id=channel_id,
                user_id=payload["user"],
                role="user",
                content=user_query
            )
            
            assistant_role = ChatHistory(
                channel_id=channel_id,
                user_id=payload["user"],
                role="assistant",
                content=data.response,
                docs_reffered=source_str
            )
            
            session.add_all([user_role, assistant_role])
            session.commit()
        except Exception as e:
            print(f"Error saving chat history: {e}")
            
        response_blocks = []
        
        if data.query_type != 'chitchat':
            response_blocks = get_response_block_with_actions(quoted_response, data.response_type)
        else:
            response_blocks = get_response_block(quoted_response)

        try:
            if loader_activated:
                client.chat_update(
                    channel=channel_id,
                    ts=message['ts'],
                    text=data.response,
                    blocks=response_blocks
                )
            else:
                client.chat_postMessage(
                    channel=channel_id,
                    user=user_id,
                    text=data.response,
                    blocks=response_blocks
                )
        except SlackApiError as e:
            print("Error sending message: {}".format(e.response["error"]))


@app.action("feedback_thumbs_down")
def handle_thumbs_down(ack, body, client):
    ack()
    
    channel_id = body["channel"]["id"]
    user_id = body.get("user", {}).get("id", "")
    thread_ts = body.get("container", {}).get("message_ts", "")
    is_ephemeral = body.get("container").get("is_ephemeral", "")
    
    try:
        chat_history = session.query(ChatHistory).filter(
            ChatHistory.channel_id == channel_id,
            ChatHistory.role == "assistant"
        ).first()
        chat_history.neg_feedback = True
        session.commit()
    except Exception as e:
        print(f"Error updating chat history: {e}")
        
    action_block = get_actions_block(type="thumbs_down")
    
    if is_ephemeral:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            thread_ts=thread_ts,
            text="Sorry to hear that, you can raise the ticket below.",
            blocks=action_block
        )
    else:  
        client.chat_postMessage(
            channel=channel_id,
            text="Sorry to hear that, you can raise the ticket below.",
            blocks=action_block
        )

@app.action("feedback_thumbs_up")
def handle_thumbs_up(ack, body, client):
    ack()
    channel_id = body["channel"]["id"]
    user_id = body.get("user", {}).get("id", "")
    thread_ts = body.get("container", {}).get("thread_ts", "")
    is_ephemeral = body.get("container", {}).get("is_ephemeral", "")
    
    try:
        chat_history = session.query(ChatHistory).filter(
            ChatHistory.channel_id == channel_id,
            ChatHistory.role == "assistant"
        ).first()

        chat_history.pos_feedback = True
        session.commit()
    except Exception as e:
        print(f"Error updating chat history: {e}")
        
    action_block = get_actions_block("thumbs_up")
    
    if is_ephemeral:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,  
            thread_ts=thread_ts,  
            blocks=action_block
        )
    else:  
        client.chat_postMessage(
            channel=channel_id,
            blocks=action_block
        )