import subprocess

def execute_python_code(python_code_as_string: str):
    python_code_as_string = python_code_as_string.replace("```python", "").split("```")[0]
    with open('executable.py', 'w') as f:
        f.write(python_code_as_string)
    subprocess.call("executable.py", shell=True)