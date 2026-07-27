"""
Supervisor Agent

Responsible for:
- Understanding user requests
- Classifying the supply chain domain
- Blocking unrelated requests
"""

import json

from langchain_core.messages import HumanMessage, SystemMessage

from llm import llm
from graph.state import SupplyChainState
from utils.prompt_loader import load_prompt

SUPERVISOR_PROMPT = load_prompt("supervisor.txt")

VALID_INTENTS = {
    "shipment",
    "inventory",
    "supplier",
    "incident",
    "recovery",
    "reporting",
}


def supervisor_agent(state: SupplyChainState):

    user_query = state["user_query"]

    messages = [

        SystemMessage(content=SUPERVISOR_PROMPT),

        HumanMessage(content=user_query)

    ]

    response = llm.invoke(messages)

    raw = response.content.strip()

    intent = "reporting"

    try:

        parsed = json.loads(raw)

        intent = parsed.get(
            "intent",
            "reporting"
        ).lower()

    except Exception:

        text = raw.lower()

        for value in VALID_INTENTS:

            if value in text:
                intent = value
                break

    if intent not in VALID_INTENTS:

        state["blocked"] = True

        state["response"] = (
            "❌ I can only assist with supply chain operations.\n\n"
            "Supported topics:\n"
            "- Shipment\n"
            "- Inventory\n"
            "- Supplier\n"
            "- Incident Management\n"
            "- Recovery Planning\n"
            "- Reporting"
        )

        return state

    state["blocked"] = False
    state["intent"] = intent
    state["current_agent"] = "Supervisor"

    return state