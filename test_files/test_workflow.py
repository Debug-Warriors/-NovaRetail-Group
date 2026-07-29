from graph.workflow import graph

state = {
    "messages": [],
    "user_query": "Track shipment SHP101",
    "intent": "",
    "current_agent": "",
    "tool_result": {},
    "response": "",
    "approval": False,
    "memory": {},
}

result = graph.invoke(state)

print(result["intent"])
print(result["current_agent"])
print(result["response"])