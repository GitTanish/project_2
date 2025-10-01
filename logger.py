import os
import csv
from datetime import datetime

def log_chat(session_id:str, query:str, response:str, is_crisis:bool):
    log_file = "chat_log.csv"
    fieldnames = ['timestamp','session_id','query','response', 'crisis_flag']
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode ='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp':datetime.utcnow().isoformat(),
            'session_id':session_id,
            'query':query,
            'response':response,
            'crisis_flag': is_crisis
        })

    
    