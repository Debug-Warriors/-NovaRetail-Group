"""
Shipment Agent

Responsibilities:
- Track shipments
- Check shipment delays
- Get shipment location
- Identify affected orders
- Reroute shipments
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from llm import llm

from graph.state import SupplyChainState

from utils.prompt_loader import load_prompt

from tools.shipment_tools import (
    track_shipment,
    check_shipment_delay,
    get_shipment_location,
    identify_affected_orders,
    reroute_shipment,
)

SHIPMENT_PROMPT = load_prompt("shipment.txt")


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def extract_shipment_id(query: str):

    match = re.search(r"SHP\d+", query.upper())

    if match:
        return match.group()

    return None


# -------------------------------------------------------
# Shipment Agent
# -------------------------------------------------------

def shipment_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Shipment Agent"

    shipment_id = extract_shipment_id(query)

    if shipment_id is None:
        shipment_id = memory.get("last_shipment")

    if shipment_id is None:

        state["response"] = (
            "Please provide a Shipment ID.\n\n"
            "Example: SHP101"
        )

        return state

    memory["last_shipment"] = shipment_id

    query_lower = query.lower()

    # --------------------------------------------------
    # Reroute Shipment
    # --------------------------------------------------

    if any(x in query_lower for x in [

        "reroute",

        "change route",

        "alternate route",

        "divert"

    ]):

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Shipment rerouting requires approval.\n\n"
                "Please approve to continue."
            )

            state["tool_result"] = {}

            state["memory"] = memory

            return state

        result = reroute_shipment(shipment_id)

    # --------------------------------------------------
    # Affected Orders
    # --------------------------------------------------

    elif any(x in query_lower for x in [

        "affected order",

        "affected orders",

        "orders affected"

    ]):

        result = identify_affected_orders(shipment_id)

    # --------------------------------------------------
    # Shipment Delay
    # --------------------------------------------------

    elif any(x in query_lower for x in [

        "delay",

        "late",

        "eta",

        "expected delivery"

    ]):

        result = check_shipment_delay(shipment_id)

    # --------------------------------------------------
    # Shipment Location
    # --------------------------------------------------

    elif any(x in query_lower for x in [

        "location",

        "where",

        "current location",

        "where is"

    ]):

        result = get_shipment_location(shipment_id)

    # --------------------------------------------------
    # Track Shipment
    # --------------------------------------------------

    else:

        result = track_shipment(shipment_id)

    state["tool_result"] = result

    messages = [

        SystemMessage(
            content=SHIPMENT_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Shipment Information:

{result}

Generate a professional shipment response.

Only use the supplied shipment information.
Do not invent details.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state