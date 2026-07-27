from agents.reporting_agent import reporting_agent


state = {

    "messages": [],

    "user_query":
        "Generate incident summary",

    "intent":
        "Reporting",

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


result = reporting_agent(state)

print(result["response"])