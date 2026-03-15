import subprocess
from skills.search import web_search
from skills.scraper import scrape_url
from skills.weather import get_weather
from skills.files import read_file_content, write_file_content, list_dir_content
from skills.python_runner import execute_python

def execute_shell(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.stdout else result.stderr
        return f"SHELL_OUTPUT:\n{output}"
    except Exception as e:
        return f"SHELL_ERROR: {str(e)}"

def handle_tool(tool_name, argument):
    print(f"Executing Skill: {tool_name}")
    
    try:
        if tool_name == "SHELL":
            return execute_shell(argument)
        elif tool_name == "SEARCH":
            return web_search(argument)
        elif tool_name == "SCRAPE":
            return scrape_url(argument)
        elif tool_name == "WEATHER":
            return get_weather(argument)
        elif tool_name == "READ":
            return read_file_content(argument)
        elif tool_name == "WRITE":
            # Handle WRITE: "path|content" or similar
            if "|" in argument:
                path, content = argument.split("|", 1)
                return write_file_content(path.strip(), content.strip())
            return "WRITE_ERROR: Expected 'path|content'"
        elif tool_name == "LIST":
            return list_dir_content(argument)
        elif tool_name == "PYTHON":
            return execute_python(argument)
        else:
            return f"TOOL_ERROR: Tool {tool_name} not recognized."
    except Exception as e:
        return f"TOOL_FATAL_ERROR: {str(e)}"
