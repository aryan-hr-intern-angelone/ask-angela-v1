from semantic_router import Route, HybridRouter
from semantic_router.encoders import FastEmbedEncoder, BM25Encoder

chitchat = Route(
    name='chitchat',
    utterances=[
        "How's the weather today?",
        "need your help",
        "I need some information",
        "What's up [name]",
        "How was your weekend?",
        "Hello [name]",
        "Long time no see!",
        "What do you do for fun?",
        "Did you see that news story?",
        "What’s new with you?",
        "How have you been?",
        "How was your commute?",
        "Did you hear about the traffic?",
        "How’s your morning going?",
        "Ready for the weekend?",
        "How’s life?",
        "Busy day?",
        "Had your coffee yet?",
        "Do you work from home?",
        "Any recommendations for a movie?",
        "Do you like working here?",
        "Are you into sports?",
        "Big plans this evening?",
        "I feel like I haven’t seen you in forever.",
        "Got any hobbies?",
        "How are you doing",
        "Weather is killing it today",
        "Hello mate",
    ],
    score_threshold=0.745
)

leaves = Route(
    name="leaves",
    utterances=[
        "How many leave days do I have left?",
        "Can I check my leave balance?",
        "are my available leave options?",
        "apply for a sick leave?",
        "Is sabbatical leave available?",
        "take maternity or paternity leave?",
        "How does bereavement leave work?",
        "is the process to apply for annual leave?",
        "need to take somse time off, how do I apply?",
        "carry forward unused leave days?",
        "can't take all my 10 leave days at once?",
        "How many more leaves can I take this year?",
        "kinds of leaves are offered by the company?",
        "I'm not feeling well, can I apply for medical leave?",
        "I request half-day leave?"
    ],
    score_threshold=0.8
)

hirearchy = Route(
    name="hirearchy",
    utterances=[
       "who is my manager",
       "who is my HRBP",
       "who is my CXO",
       "what is my employee hirearchy"
    ],
    score_threshold=0.75
)

valid_context = Route(
    name="valid_context",
    utterances=[
       "I can help with that. What specific information are you looking for?"
    ]
)

no_context = Route(
    name='no_context',
    utterances = [
        "The policies do not mention whether",
        "I don't have specific information about", 
        "policies do not mention specific information about",
        "I'm unable to provide details on this particular question",
        "I don't have specific information about that topic available at the moment.",
        "I’m not sure about that. My data doesn’t cover this topic.",
        "I’m sorry, I don’t see any info on that in the current documents.",
        "I am sorry I do not have the",
        "I cannot help with",
    ],
    score_threshold=0.74
)

query_routes = [chitchat, leaves, hirearchy]
response_routes = [no_context, valid_context]

dense_encoder = FastEmbedEncoder(model_name="BAAI/bge-small-en")
sparse_encoder = BM25Encoder(k1=2.0, b=0.75)

query_rl = HybridRouter(
    routes=query_routes, 
    encoder=dense_encoder, 
    # sparse_encoder=sparse_encoder, 
    auto_sync="local"
)

response_rl = HybridRouter(
    routes=response_routes, 
    encoder=dense_encoder, 
    sparse_encoder=sparse_encoder, 
    auto_sync="local"
)