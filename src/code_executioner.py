import subprocess

def execute_python_code(python_code_as_string: str):
    python_code_as_string = python_code_as_string \
        .split("```python")[1] \
        .split("```")[0]
    
    with open('executable.py', 'w') as f:
        f.write(python_code_as_string)
    
    # Capture the output
    result = subprocess.run("python3 ./executable.py", shell=True, capture_output=True, text=True)
    
    return result.stdout