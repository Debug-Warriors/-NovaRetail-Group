from graph.workflow import graph


state = {

    "messages": [],

    "user_query":
        "Track shipment SHP101",

    "intent":
        "",

    "current_agent":
        "",

    "tool_result":
        {},

    "response":
        "",

    "approval":
        False,

    "memory":
        {}

}


result = graph.invoke(state)


print("----------------")
print("Intent:")
print(result["intent"])

print("----------------")
print("Agent:")
print(result["current_agent"])

print("----------------")
print("Response:")
print(result["response"])