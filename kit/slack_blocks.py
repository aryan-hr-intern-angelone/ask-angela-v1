from typing import Literal
from kit.slack_utils import get_nocontext_response, get_feedback_repsponse

def get_hello_block(fname: str):
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi {fname}, Welcome to Ask Angela, your assistant for HR queries. Ask any question and get answers in seconds! Please note that Ask Angela is still in development. If you believe an answer may be incorrect, we recommend verifying it with your HRBP directly."
        }
    }]

def get_response_block(response: str):
    return [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": response        
        }
    }]

def get_response_block_with_actions(response: str, type: Literal["no_context", None] = None):
    response_blocks = [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": response        
        }
    }]

    if type == "no_context":
        nocontext_response = get_nocontext_response()
        response_blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Raise Ticket",
                                "emoji": True
                            },
                            "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                            "action_id": "raise_ticket_click"
                        }
                    ]
                }
        ])
    else:
        default_response = get_feedback_repsponse()
        response_blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{default_response}"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👍"
                        },
                        "value": "thumbs_up",
                        "action_id": "feedback_thumbs_up"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👎"
                        },
                        "value": "thumbs_down",
                        "action_id": "feedback_thumbs_down"
                    }
                ]
            }
        ])
    
    return response_blocks

def get_feedback_block(type: Literal["no_context", None] = None):
    if type == "no_context":
        nocontext_response = get_nocontext_response()
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Raise Ticket",
                                "emoji": True
                            },
                            "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                            "action_id": "raise_ticket_click"
                        }
                    ]
                }
        ]
    else:
        default_response = get_feedback_repsponse()
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{default_response}"
                }
            }, {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👍"
                        },
                        "value": "thumbs_up",
                        "action_id": "feedback_thumbs_up"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "👎"
                        },
                        "value": "thumbs_down",
                        "action_id": "feedback_thumbs_down"
                    }
                ]
            }
        ]
        
def get_actions_block(type: Literal["thumbs_up", "thumbs_down"]):
    if type == "thumbs_down":
        nocontext_response = get_nocontext_response(type="actions")
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{nocontext_response}"
                }
            },
            {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Raise Ticket",
                                "emoji": True
                            },
                            "url": "https://hrsupport.angelone.in/hc/en-us/requests/new?ticket_form_id=5893162753309",
                            "action_id": "raise_ticket_click"
                        }
                    ]
                }
        ]
    else:
        return [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Thank you so much for your positive feedback."
                }
            }
        ]