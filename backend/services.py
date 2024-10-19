import os
import sqlite3
from openai import OpenAI

from dotenv import load_dotenv

client = OpenAI(api_key="sk-EWOP-jzilwNYFK3TOOQlu46YycCaX9uIFWNuU8LiVuT3BlbkFJ4A5VpTj-ewmHJz0b6dOc_Wqg8ooC7_EUjcMKy_4KIA")


def enviar_mensagem(mensagem):
    # Conectando ao banco de dados
    conn = sqlite3.connect('chat_messages.db')
    cursor = conn.cursor()

    # Obtendo todas as mensagens do banco de dados
    cursor.execute('SELECT role, content FROM messages')
    rows = cursor.fetchall()
    
    # Criando um array para armazenar as mensagens
    mensagens_api = []
    for row in rows:
        role, content = row  # Desempacotando a tupla
        mensagens_api.append({"role": role, "content": content})  # Formatando como dicionário

    # Adicionando a nova mensagem ao array
    mensagens_api.append({"role": "user", "content": mensagem})  # Adiciona a nova mensagem

    # Fazendo a chamada para a API OpenAI
    resposta = client.chat.completions.create(model="gpt-4o-mini", messages=mensagens_api)
    
    # Fechando a conexão com o banco de dados
    conn.close()

    # # Acesso correto à resposta
    # if resposta.choices and len(resposta.choices) > 0:
    #     message_content = resposta.choices[0].message.content[0].text
    #     annotations = message_content.annotations
    #     citations = []
    # #    Iterate over the annotations and add footnotes
    #     for index, annotation in enumerate(annotations):
    # # Replace the text with a footnote
    #         message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
    # # Gather citations based on annotation attributes
    #         if (file_citation := getattr(annotation, 'file_citation', None)):
    #             cited_file = client.files.retrieve(file_citation.file_id)
    #             citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
    #         elif (file_path := getattr(annotation, 'file_path', None)):
    #             cited_file = client.files.retrieve(file_path.file_id)
    #             citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
    #     # Note: File download functionality not implemented above for brevity
    # # Add footnotes to the end of the message before displaying to user
    #     message_content.value += '\n' + '\n'.join(citations)
    # else:
    #     print("Nenhuma escolha encontrada na resposta da API.")
    #     return None

 #   print(message_content.value)
    
    return resposta.choices[0].message.content

def save_message(role, content):
    conn = sqlite3.connect('chat_messages.db')

    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    
    conn.commit()
    conn.close()

def process_request(request):
    response = enviar_mensagem(request)
    save_message("user", request)
    save_message("assistant", response)

    return response

def execute_generated_query(query):
    conn = sqlite3.connect('chat_messages.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

