from agents.inventory_agent import inventory_agent


state = {
    "messages": [],
    "user_query": "Check stock for product P200",
    "intent": "Inventory",
    "current_agent": "",
    "tool_result": {},
    "response": "",
    "approval": False,
    "memory": {}
}


result = inventory_agent(state)

print(result["response"])