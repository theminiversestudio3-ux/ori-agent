import os
import requests
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from memory import get_system_prompt
from tools import handle_tool

load_dotenv()

LOCAL_API_URL = "http://localhost:8080/v1/chat/completions"
MODEL = "local-model"

app = Flask(__name__)
chat_history = []

def call_local_llm(messages):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.2, # Low temperature for reliable tool tags
        "max_tokens": 1024
    }
    try:
        response = requests.post(LOCAL_API_URL, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error connecting to local model: {str(e)}"

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    data = request.json
    user_msg = data.get("message")
    if not user_msg: return jsonify({"error": "No message"}), 400

    system_prompt = get_system_prompt()
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(chat_history[-6:])
    messages.append({"role": "user", "content": user_msg})
    
    response = call_local_llm(messages)
    
    # RECURSIVE REASONING LOOP (Max 5 steps for complex tasks)
    for i in range(5):
        # Look for [TOOL_NAME: argument]
        # Regex handles [NAME: arg] but also captures THOUGHTs to ignore them for execution
        match = re.search(r"\[(SEARCH|SCRAPE|WEATHER|SHELL|READ|WRITE|LIST|PYTHON): (.*?)\]", response)
        
        if not match:
            break
            
        tool_name = match.group(1)
        argument = match.group(2)
        
        # Execute tool
        print(f"ULTRA_LOOP Step {i+1}: Executing {tool_name}")
        output = handle_tool(tool_name, argument)
        
        # Feed back to LLM as an observation
        messages.append({"role": "assistant", "content": response})
        messages.append({"role": "user", "content": f"OBSERVATION from {tool_name}:\n{output}\nBased on this, what is the next step or final answer?"})
        
        # Get next thought/action
        response = call_local_llm(messages)
    
    chat_history.append({"role": "user", "content": user_msg})
    chat_history.append({"role": "assistant", "content": response})
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
