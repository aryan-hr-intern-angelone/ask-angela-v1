from database.dm_integration import get_connection_pool
from utils.darwinbox import darwinbox_leavebalance

def get_leavebalance(email: str):
    pool = get_connection_pool()
    emp_id = ""
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as curr:
                    curr.execute("SELECT employeeid FROM tsm.activeheadcount WHERE LOWER(angelone_email) = (%s) OR LOWER(email) = (%s)", (email,email,))
                    result = curr.fetchone()
                    if result:
                        emp_id = result[0]
    except Exception as e:
        print("Error Finding Employee Details")
        
    return darwinbox_leavebalance(emp_id) if emp_id else ""