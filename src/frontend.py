import streamlit as st
import time
from math_to_solution import math_to_code, text_to_math
from code_executioner import execute_python_code


def process_task(task_description):
    # Simulating work
    time.sleep(2)
    return f"Task '{task_description}' has been processed successfully!"

st.title("Task Processing Dashboard")

task_description = st.text_area("Enter your task description:")

if st.button("Process Task"):
    if task_description:
        st.write("Processing task...")
        
        # Step 1: Formalizing problem
        st.subheader("Step 1: Formalizing problem")
        with st.spinner("Working on formalizing the problem..."):
            translated_task_description = text_to_math(task_description)

        st.success("Problem formalized!")
        with st.expander("View formalized problem", expanded=False):
            st.write(f"Formalized problem: {translated_task_description}")
        
        # Step 2: Transforming problem into code
        st.subheader("Step 2: Transforming problem into code")
        with st.spinner("Working on transforming the problem into code..."):
            solution = math_to_code(translated_task_description)
        st.success("Problem transformed into code!")
        with st.expander("View generated code", expanded=False):
            st.code(solution, language="python")
        
        # Step 3: Running code
        st.subheader("Step 3: Running code")
        with st.spinner("Running code..."):
            result = execute_python_code(solution)
        st.success("Code execution completed!")

        with st.expander("View execution details", expanded=False):
            st.write(result)
        
        # Display the final result
        st.subheader("Task Result")
        st.markdown(result)
    else:
        st.warning("Please enter a task description.")