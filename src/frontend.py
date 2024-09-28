import streamlit as st
import time



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
            time.sleep(2)  # Simulating work
        st.success("Problem formalized!")
        
        # Step 2: Transforming problem into code
        st.subheader("Step 2: Transforming problem into code")
        with st.spinner("Working on transforming the problem into code..."):
            time.sleep(2)  # Simulating work
        st.success("Problem transformed into code!")
        
        # Step 3: Running code
        st.subheader("Step 3: Running code")
        with st.spinner("Running code..."):
            result = process_task(task_description)
        st.success("Code execution completed!")
        
        # Display the result
        st.subheader("Task Result")
        st.markdown(result)
    else:
        st.warning("Please enter a task description.")