import subprocess

def execute_python_code(python_code_as_string: str):
    python_code_as_string = "import" + python_code_as_string \
        .replace("```python", "") \
        .split("```")[0] \
        .split("import")[1]
    
    with open('executable.py', 'w') as f:
        f.write(python_code_as_string)
    subprocess.call("python3.11 ./executable.py", shell=True)