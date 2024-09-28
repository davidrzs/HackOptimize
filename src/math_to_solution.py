import time

from ai21 import AI21Client
from ai21.models.chat import ChatMessage

model = "jamba-1.5-mini"

client = AI21Client(
    api_key="6tHa1Ly9bLfewfSO3gqnYRBQ15FFBhhl",
)


def text_to_math(task_description: str):
    messages_step1 = [
        ChatMessage(content="""
                            You are an Operations Research scientist. You are trying to solve a scheduling problem.
                            You will be given a problem and you will need to translate it into mathematical notation.
                            Your task is to translate the problem into an optimization problem.

                            The problem should be formulated with one the following objectives:
                            1. Minimize time from start to finish of all required jobs
                            2. Minimize resource consumed
                            3. Minimize downtime between jobs
                            4. Maximize an output like number of items produced or profit


                            Decisions variables can for example be:
                            1. Start time for each job, machine pair
                            2. Makespan completion
                            3. Number of items produced by each machine

                            Constraints can for example be:
                            1. Each job must be done once
                            2. Each machine can only do one job at a time
                            3. Each job must be done in a certain order
                            4. Each job must be done within a certain time frame
                            5. Maximum number of jobs that can be done in a day
                            6. There might be downtime required between jobs

                            The problem should be formulated in the following format, :
                            Objective function: Minimize or Maximize
                            Decision variables: x1, x2, x3, ...
                            Constraints: c1, c2, c3, ...
                            """, role="system"),
        ChatMessage(content=task_description, role="user"),
    ]
    chat_completions = client.chat.completions.create(
                messages=messages_step1,
                model=model,
            )

    return chat_completions.choices[0].message.content

def math_to_code(math_input: str):
    messages_step2 = [
            ChatMessage(content="You are professional softeare engineer", role="system"),
            ChatMessage(content="transform this solution into python executable code", role="user"),
            ChatMessage(content=math_input, role="user"),
    ]
    chat_completions = client.chat.completions.create(
                messages=messages_step2,
                model=model,
            )
    return chat_completions.choices[0].message.content
    


def process_task(task_description):
    # Simulating work
    time.sleep(2)
    return f"Task '{task_description}' has been processed successfully!"
