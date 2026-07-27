from agents.recovery_agent import recovery_agent


state = {

    "messages": [],

    "user_query":
        "Create recovery plan for delayed shipment SHP101 P100",

    "intent":
        "Recovery",

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


result = recovery_agent(state)


print(result["response"])