from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import Config, Server
from lib.rag import user_input
import asyncio

app = FastAPI()

class MessageBody(BaseModel):
    query: str
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/message")
def handle_user_message(body: MessageBody):
    result = user_input(body.query, "", "")
    print(result.response)
    return {
        'query': result.query,
        'response': result.response
    }
   
def run_server():
    config = Config("api.route:app", host="0.0.0.0", port=3000, reload=True)
    server = Server(config)
    asyncio.run(server.serve())
