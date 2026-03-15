import sys
import io
import contextlib

def execute_python(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            # Using a shared global dict for simple persistence across calls if needed
            exec(code, {})
        return f"PYTHON_OUTPUT:\n{output.getvalue()}"
    except Exception as e:
        return f"PYTHON_ERROR:\n{str(e)}"
