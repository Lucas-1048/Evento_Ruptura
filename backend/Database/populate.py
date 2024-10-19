import sqlite3
import pandas as pd

def initialize_databases():
    chat_messages_db_path = './backend/Database/chat_messages.db'
    vehicles_db_path = './backend/Database/ruptura_vehicles.db'
    vehicles_csv_path = './backend/Database/ruptura_vehicles.csv'

    init_messages_database(chat_messages_db_path)
    populate_vehicles_database(vehicles_csv_path, vehicles_db_path)

def init_messages_database(db_file_path):
    conn = None
    try:
        conn = sqlite3.connect(db_file_path)

        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

        print("Tabela 'messages' criada com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def populate_vehicles_database(csv_file_path, db_file_path, table_name = "vehicles"):
    conn = None
    try:
        df = pd.read_csv(csv_file_path)
        conn = sqlite3.connect(db_file_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)

        conn.commit()
        conn.close()

        print(f"Tabela '{table_name}' criada e populada com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")