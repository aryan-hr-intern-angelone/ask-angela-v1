import csv
import time
from lib.rag import user_input

# with open('policy_faqs_20250707_180002.csv', 'r') as file:
#     reader = csv.reader(file)
#     rows = list(reader)

# responses = []
# header = rows[0] + ['AskAngela Response']
# responses.append(header)

# try:
#     for row in rows[596:]:
#         query = row[2]
#         data = user_input(query, "test_channel", "test_user")
#         time.sleep(3)
#         row.append(data.response)
#         responses.append(row)

#     with open('custom_data.csv', 'w', newline='') as output_file:
#         writer = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
#         writer.writerows(responses)          
# except Exception as e:
#     with open('custom_data.csv', 'w', newline='') as output_file:
#         writer = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
#         writer.writerows(responses)
    # raise e
    
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    
responses = []
header = rows[0] + ['AskAngela Response']
responses.append(header)

try:
    for row in rows[1:]:
        query = row[0]
        data = user_input(query, "test_channel", "test_user")
        time.sleep(2)
        new_row = row + [data.response]
        responses.append(new_row)
        
    with open('custom_queries.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(responses)
except Exception as e:
    with open('custom_queries.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(responses)
    raise e
