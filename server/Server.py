import os
import shutil
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import setuptools
import logging
from llama_index.prompts import Prompt
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage
from llama_index.chat_engine import CondenseQuestionChatEngine


# Write a funktion that reads the file ChatGPT.txt which is two levels up from the current
# directory and returns the content of the file as a string

# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1

def read_file():
    print("Current Working Directory:", os.getcwd())
    with open('../../APIKey/ChatGPT.txt', 'r') as file:
        data = file.readline()
        return data.strip()

os.environ["OPENAI_API_KEY"] = read_file()

app = Flask(__name__)
CORS(app)

def verify_index_success(index_dir):
    # Überprüfung, ob das Verzeichnis existiert und nicht leer ist
    if not os.path.exists(index_dir) or not os.listdir(index_dir):
        return False

    # Beispiel: Überprüfung auf eine spezifische Datei, die nach erfolgreicher Indexierung vorhanden sein sollte
    expected_file = os.path.join(index_dir, 'index_metadata.json')
    if not os.path.exists(expected_file):
        return False

    # Optional: Überprüfen der Dateigröße oder des Inhalts spezifischer Dateien
    # Hier können Sie beispielsweise öffnen und den Inhalt von 'index_metadata.json' prüfen,
    # um sicherzustellen, dass er gültige Metadaten enthält.

    # Weitere spezifische Überprüfungen je nach Anforderung
    # ...

    return True  # Wenn alle Überprüfungen erfolgreich sind


def create_llama_index():
    try:
        print("Indexing document")
        index_dir = 'index' # Specify the directory where you want to store the index
        os.makedirs(index_dir, exist_ok=True) # Create the directory if it does not exist
        documents = SimpleDirectoryReader('uploads').load_data() # Load the documents from the directory
        index = GPTVectorStoreIndex.from_documents(documents)        
        index.storage_context.persist(index_dir) # Stores the created index in the specified directory which is index in this case
        if not os.path.exists(index_dir) or not os.listdir(index_dir): # Check if the index directory is empty
            raise Exception("No Document saved")
        if not verify_index_success(index_dir):
            raise Exception("Indexing document failed")

        print("Indexing document successful")
        return jsonify({'message': 'File indexed successfully'})
    except Exception as e:
        return f"An error occured: {e}", 400
    

def get_custom_prompt():
    try:
        print('get_custom_prompt called')
        return Prompt("""\
Rephrase the conversation and subsequent message into 
a self-contained question while including all relevant details. 
Conclude the question with: Only refer to this document.

<Chat History> 
{chat_history}

<Follow Up Message>
{question}

<Standalone question>
""")
    except Exception as e:
        # If an error occurs during the try block, catch it here
        print('error in get_custom_prompt: ', e)
        return jsonify({'error':  f"An error occurred: {e}"})

# creates chat history
    
def getChatHistory(history='[]'):
    try:
        from llama_index.llms import ChatMessage, MessageRole
        history = json.loads(history)

        # initialize chart history
        custom_chat_history = []
        roles = {"left_bubble": "ASSISTANT", "right_bubble": "USER"}
        for chat in history:
            position = chat['position']
            role = MessageRole[roles[position]]
            content = chat['message']
            custom_chat_history.append(
                ChatMessage(
                    # can be USER or ASSISTANT
                    role=role,
                    content=content
                )
            )
        return custom_chat_history
    except Exception as e:
        # If an error occurs during the try block, catch it here
        return jsonify({'error':  f"An error occurred: {e}"})

def query_index():
    # retrive open ai key
    try:
        index_dir = 'index'

        if not os.path.exists(index_dir) or not os.listdir(index_dir):
            return jsonify({'error':  f"Index directory '{index_dir}' does not exist or is empty."})
        data = request.get_json() # decode json from frontend
        prompt = data.get('prompt') # data extracted from json by using prompt key
        chatHistory = data.get('chatHistory')
        
        storage_context = StorageContext.from_defaults(persist_dir=index_dir)
        index = load_index_from_storage(storage_context) # load index and set up chat engine
        query_engine = index.as_query_engine()
        chat_engine = CondenseQuestionChatEngine.from_defaults(
            query_engine=query_engine,
            condense_question_prompt=get_custom_prompt(), # direct the llama index
            chat_history=getChatHistory(chatHistory),
            verbose=True
        )

        response_node = chat_engine.chat(prompt)  # chat here
        return jsonify({'result':  response_node.response})

    except Exception as e:
        return jsonify({'error':  f"An error occurred: {e}"})
    
def delete_all_data():
    try:
        shutil.rmtree('uploads')
        shutil.rmtree('index')
        print('All data deleted')
    except Exception as e:
        print('An error occured: ', e)
        





@app.route('/')
def hello_world():
    return "hello world!"

@app.route('/ask_ai', methods=['POST'])
def query_endpoint():
    response = query_index()
    print('route ask_ai called')
    return response

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        upload_dir = 'uploads' # Secify the directory where you want to
        os.makedirs(upload_dir, exist_ok=True)

        file.save(os.path.join(upload_dir, file.filename))

        print('File uploaded successfully')

        return create_llama_index()
    
@app.route('/delete_all_data', methods=['POST'])
def delete_data():
    delete_all_data()
    return jsonify({'message': 'All data deleted successfully'})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)