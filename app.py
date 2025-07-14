import threading
from slack_app.slack_socket import handler
from api.route import run_server
from lib.aws import document_listener
# from test import test

def main():
    document_listener_thread = threading.Thread(target=document_listener, daemon=True)
    slack_thread = threading.Thread(target=handler.start, daemon=True)
    # api_thread = threading.Thread(target=run_server, daemon=True)
    # test_thread = threading.Thread(target=test(), daemon=True) 
    
    document_listener_thread.start()
    slack_thread.start()
    # api_thread.start()
    # test_thread.start()
    
    document_listener_thread.join()
    slack_thread.join()
    # api_thread.join()
    # test_thread.join()
    
if __name__ == "__main__":
    main()