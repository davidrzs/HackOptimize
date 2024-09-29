from ai21 import AI21Client
from ai21.logger import set_verbose
from ai21.models.chat import ChatMessage, ToolMessage
from ai21.models.chat.function_tool_definition import FunctionToolDefinition
from ai21.models.chat.tool_defintions import ToolDefinition
from ai21.models.chat.tool_parameters import ToolParameters
import json, requests
from openai import OpenAI

client = AI21Client(api_key='kXftEvJYqotOSkpTw1e2KNUhvYX0EvU1')

model = "jamba-1.5-large"



def translate_to_math(input):

    messages = [ChatMessage(content=
                            """
                            You are an Operations Research scientist. You are trying to solve a scheduling problem.
                            You will be given a problem and you will need to translate it into mathematical notation.
                            Your task is to translate the problem into an optimization problem.

                            The problem should be formulated with the following objective:
                            
                            Minimize time from start to finish of all required jobs

                            Decisions variables will be:
                            
                            Start time for each job, machine pair

                            Constraints can be:
                            
                            Each job must be done once
                            Each machine can only do one job at a time
                            Each job must be done within a certain time frame
                            
                            Your answer must be self-contained and complete so that someone else can understand it without any additional context.
                            """, role="system")]
    messages.append(ChatMessage(content="This is the problem: " + input, role="user"))
    response = client.chat.completions.create(
      messages=messages,
      model=model,
      stream=True
    )
    for chunk in response:
      print(chunk.choices[0].delta.content, end="")