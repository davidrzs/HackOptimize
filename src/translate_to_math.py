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

                            Write all constraints inividually such that it is immediately clear what each constraint is.
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