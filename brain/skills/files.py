import os

def read_file_content(path):
    try:
        with open(path, 'r') as f:
            return f"FILE_CONTENT ({path}):\n{f.read()}"
    except Exception as e:
        return f"Error reading file {path}: {str(e)}"

def write_file_content(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file {path}: {str(e)}"

def list_dir_content(path="."):
    try:
        files = os.listdir(path)
        return f"DIRECTORY_CONTENT ({path}):\n" + "\n".join(files)
    except Exception as e:
        return f"Error listing directory {path}: {str(e)}"
