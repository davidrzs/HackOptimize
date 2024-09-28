import time

from ai21 import AI21Client
from ai21.models.chat import ChatMessage

model = "jamba-1.5-mini"

client = AI21Client(
    api_key="6tHa1Ly9bLfewfSO3gqnYRBQ15FFBhhl",
)


def text_to_math(task_description: str):
    messages_step1 = [
        ChatMessage(content="You're a designed to resolve scheduling problems", role="system"),
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
