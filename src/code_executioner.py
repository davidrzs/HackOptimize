import subprocess

def execute_python_code(python_code_as_string: str):
    python_code_as_string = python_code_as_string \
        .replace("```python", "") \
        .split("```")[0] \
        .split("import")[1:]
    
    with open('executable.py', 'w') as f:
        for python_code_line in python_code_as_string[1:]:
            f.write("import"+python_code_line)
    subprocess.call("python3 ./executable.py", shell=True)