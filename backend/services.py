import os
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def send_message(mensagem):
    db_file_path = './backend/Database/chat_messages.db'
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute('SELECT role, content FROM messages ORDER BY id')
    rows = cursor.fetchall()
    
    mensagens_api = []
    for row in rows:
        role, content = row 
        mensagens_api.append({"role": role, "content": content})

    mensagens_api.append({"role": "user", "content": mensagem})

    resposta = client.chat.completions.create(model="gpt-4o-mini",
        messages=mensagens_api
    )
    
    conn.close()
    
    return resposta.choices[0].message.content

def save_message(role, content):
    db_file_path = './backend/Database/chat_messages.db'

    try:
        conn = sqlite3.connect(db_file_path)

        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
        
        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def process_request(request):
    save_message("user", request)
    response = send_message(request)
    save_message("assistant", response)

    return response

def execute_generated_query(query):
    db_file_path = './backend/Database/ruptura_vehicles.db'

    try:
        conn = sqlite3.connect(db_file_path)

        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        conn.close()
        return results
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None
