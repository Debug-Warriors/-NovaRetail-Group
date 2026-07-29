from llm import llm

response = llm.invoke("Hello! Who are you?")

print(response.content)