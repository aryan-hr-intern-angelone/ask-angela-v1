import time
import json
import hashlib
import requests
from config.env import env
    
def sha512_hash(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    hasher = hashlib.sha512()
    hasher.update(text)
    return hasher.hexdigest()

def stringify_leavebalance(leave_data):
    leave_summary = "---- Leave History Details ----\n"
    for data in leave_data[:-1]:
        leave_summary += f'''
        Leave Type: {data["leave_name"]}
        - Currently Available Balance: {data["currently_availabel_balance"]} 
        - Accrued So Far: {data["accrued_so_far_this_year"]}
        - Previous Balance: {data["previous_balance"]}
        - Adjustment Balance: {data["adjustment_balance"]}
        - Yearly Allotment: {data["yearly_allotment"]},
        - Taken: {data["taken"]}
        - Utilized Leaves This Year: {data["utilized_leaves_this_year"]}
        '''
    
    # final = leave_data[-1:]
    # if final:
    #     leave_summary += f'''
    #     Leave Type: {final[0]["leave_name"]}
    #     - Already Taken: {final[0]["already_taken"]}
    #     - Applied Unpaid: {final[0]["applied_unpaid"]}
    #     - System Unpaid: {final[0]["system_unpaid"]}
    #     '''
    
    return leave_summary

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
     

    