import time
import json
import hashlib
import requests
from config.env import env
from lib.format import stringify_leavebalance
    
def sha512_hash(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    hasher = hashlib.sha512()
    hasher.update(text)
    return hasher.hexdigest()

def darwinbox_leavebalance(*employees):
    emp_ids = [emp for emp in employees]
    timestamp = str(int(time.time()))
    
    comb = env.darwinbox.DARWINBOX_API_KEY + env.darwinbox.DARWINBOX_API_SECRET + timestamp
    hash = sha512_hash(comb)
    
    headersList = {
        "Accept": "*/*",
        "Content-Type": "application/json" 
    }
    
    payload_body = json.dumps({
        "timestamp": timestamp,
        "hash": hash,
        "Uid": env.darwinbox.DARWINBOX_API_UID,
        "employee_nos": emp_ids
    })
    
    response = requests.post(
        url=env.darwinbox.DARWINBOX_API_URL,
        headers=headersList,
        data=payload_body
    )
    
    data = response.json()["data"]
    leave_summary = stringify_leavebalance(data)
    return leave_summary
     

    