import os

def read_memory():
    try:
        with open('ori-agent/brain/MEMORY.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def read_soul():
    try:
        with open('ori-agent/brain/SOUL.md', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def update_memory(new_fact):
    with open('ori-agent/brain/MEMORY.md', 'a') as f:
        f.write(f"\n- (Auto-added on 2026-03-15) {new_fact}")

def get_system_prompt():
    soul = read_soul()
    memory = read_memory()
    return f"""
{soul}

## User Context (MEMORY)
{memory}

## CRITICAL: TOOL USE RULES
You are a recursive AI agent. For complex tasks, you MUST use tools to gather data or execute actions. 
DO NOT finish the task until you have all the data. Use [THOUGHT: <your reasoning>] before using a tool.

AVAILABLE TOOLS:
1. [SEARCH: <query>] - Web search.
2. [SCRAPE: <url>] - Read website text.
3. [WEATHER: <city>] - Current weather.
4. [SHELL: <cmd>] - Shell commands.
5. [READ: <path>] - Read a local file.
6. [WRITE: <path>|<content>] - Write to a local file.
7. [LIST: <path>] - List directory content.
8. [PYTHON: <code>] - Execute Python code.

EXAMPLES:
- User: "Summarize the files in this folder."
  Assistant: "[THOUGHT: I need to list the files first.] [LIST: .]"
- User: "Write a python script to hello.py and run it."
  Assistant: "[THOUGHT: I'll write the file first.] [WRITE: hello.py|print('hello')] [THOUGHT: Now I run it.] [SHELL: python3 hello.py]"
"""
