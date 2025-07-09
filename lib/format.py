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

def stringify_hierarchy(data):
    if not data:
        return "No Employee Details Available"
    
    designation = {
        "employeename": "Employee Name",
        "manager_name": "Manager Name",
        "hrbpname": "HRBP Name",
        "cxo": "CXO",
        "l1leadername": "L1 Leader Name",
        "l2leadername": "L2 Leader Name",
        "l3leadername": "L3 Leader Name",
        "l4leadername": "L4 Leader Name",
        "l5leadername": "L5 Leader Name",
        "l6leadername": "L6 Leader Name",
        "l7leadername": "L7 Leader Name",
        "l8leadername": "L8 Leader Name"
    }
    
    hierarchy_details = "---- Employee Hierarchy Details ----\n"
    for key, value in data.items():
        if value:
            hierarchy_details += f"{designation[key]} : {value}\n"
    
    return hierarchy_details