"""
Supervisor Agent

Responsible for:
- Understanding user requests
- Classifying the supply chain domain
- Routing requests to the correct agent
- Blocking unsupported requests
"""

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

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

    "risk",

    "general",

    "unsupported",
}


def supervisor_agent(state: SupplyChainState):

    user_query = state["user_query"].strip()


    query = user_query.lower().strip()

    # ----------------------------------------------------
    # Greetings
    # ----------------------------------------------------

    if query in {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    }:

        state["blocked"] = False
        state["intent"] = "general"
        state["current_agent"] = "Supervisor"

        return state


    messages = [

        SystemMessage(
            content=SUPERVISOR_PROMPT
        ),

        HumanMessage(
            content=user_query
        )

    ]

    response = llm.invoke(messages)

    print("=" * 60)
    print("RAW SUPERVISOR RESPONSE:")
    print(repr(response.content))
    print("=" * 60)

    intent = response.content.strip().lower()

    # Clean extra whitespace/newlines
    intent = intent.replace("\n", "").replace("\r", "").strip()

    print("Detected Intent:", intent)

    # Safety fallback
    if intent not in VALID_INTENTS:
        intent = "unsupported"

    # ----------------------------------
    # Unsupported request
    # ----------------------------------

    if intent == "unsupported":

        state["blocked"] = True

        state["current_agent"] = "Supervisor"

        state["intent"] = "unsupported"

        state["response"] = (
            "❌ This assistant only supports **NovaRetail Supply Chain Operations**.\n\n"
            "Supported capabilities:\n\n"
            "📦 Shipment Tracking\n"
            "📦 Inventory Management\n"
            "🏢 Supplier Management\n"
            "⚠ Incident Management\n"
            "🔄 Recovery Planning\n"
            "📊 Operational Reporting\n"
            "🧠 Predictive Risk Intelligence\n\n"
            "Please ask a supply chain-related question."
        )

        return state

    # ----------------------------------
    # Valid request
    # ----------------------------------

    state["blocked"] = False

    state["intent"] = intent

    state["current_agent"] = "Supervisor"

    return state