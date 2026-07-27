from agents.supervisor import supervisor_agent


state = {
    "messages": [],
    "user_query": "Track shipment SHP101",
    "intent": "",
    "current_agent": "",
    "tool_result": {},
    "response": "",
    "approval": False,
    "memory": {}
}


result = supervisor_agent(state)


print(result["intent"])