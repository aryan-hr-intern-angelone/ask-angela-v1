from database.dm_integration import get_connection_pool
from psycopg.rows import dict_row
from lib.format import stringify_hierarchy
from lib.darwinbox import darwinbox_leavebalance

def get_leavebalance(email: str):
    pool = get_connection_pool()
    emp_id = ""
    
    try:
        with pool.connection() as conn:
            with conn.cursor() as curr:
                    curr.execute('''
                        SELECT employeeid 
                        FROM employees
                        WHERE LOWER(angelone_email) = (%s) 
                        OR LOWER(email) = (%s)
                        OR angelone_email = (%s)
                        OR email = (%s)
                    ''', (email,email,email,email,))
                    result = curr.fetchone()
                    print(result)
                    if result:
                        emp_id = result[0]
    except Exception as e:
        print("Error Finding Employee Leave Details")
        
    return darwinbox_leavebalance(emp_id) if emp_id else ""

def get_hierarchy(email: str):
    pool = get_connection_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as curr:
                curr.execute('''
                    SELECT manager_name, hrbpname, cxo, l1leadername, l2leadername, l3leadername, l4leadername, l5leadername, l6leadername, l7leadername, l8leadername
                    FROM employees
                    WHERE LOWER(angelone_email) = (%s)
                    OR LOWER(email) = (%s)
                    OR angelone_email = (%s)
                    OR email = (%s)
                ''', (email,email,email,email))
                result = curr.fetchone()
                print(result)
    except Exception as e:
        print("Error Finding Employee Hirearchy Details")
        
    return stringify_hierarchy(result)