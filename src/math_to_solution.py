# from ai21 import AI21Client

# messages = [ChatMessage(content="Who was the first emperor of rome", role="user")]

# client = AI21Client()

# response = client.chat.completions.create(
#   messages=messages,
#   model="jamba-1.5-mini",
#   stream=True
# )

# for chunk in response:
#   print(chunk.choices[0].delta.content, end="")

def math_to_solution(input):
    return input