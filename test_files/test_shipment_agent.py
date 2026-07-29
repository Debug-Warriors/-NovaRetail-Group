from agents.shipment_agent import shipment_agent


state = {

    "messages": [],

    "user_query":
        "Track shipment SHP101",

    "intent":
        "Shipment",

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


result = shipment_agent(state)


print(result["response"])