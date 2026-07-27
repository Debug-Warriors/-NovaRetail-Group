"""
Shipment Agent

Responsibilities:
- Track shipments
- Check shipment delays
- Get shipment location
- Identify affected orders
- Reroute shipment
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
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


def extract_shipment_id(query: str):

    match = re.search(
        r"SHP\d+",
        query.upper()
    )

    if match:
        return match.group()

    return None


def shipment_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Shipment Agent"

    shipment_id = extract_shipment_id(query)

    if shipment_id is None:
        shipment_id = memory.get("last_shipment")

    if shipment_id is None:

        state["response"] = (
            "Please provide a Shipment ID.\n"
            "Example: SHP101"
        )

        return state

    memory["last_shipment"] = shipment_id

    query_lower = query.lower()

    # ---------------------------------------
    # Reroute Shipment
    # ---------------------------------------

    if (
        "reroute" in query_lower
        or "change route" in query_lower
    ):

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Rerouting a shipment requires approval.\n\n"
                "Press 'Approve' to continue."
            )

            state["tool_result"] = {}
            state["memory"] = memory

            return state

        result = reroute_shipment(shipment_id)

    # ---------------------------------------
    # Affected Orders
    # ---------------------------------------

    elif (
        "affected order" in query_lower
        or "affected orders" in query_lower
    ):

        result = identify_affected_orders(
            shipment_id
        )

    # ---------------------------------------
    # Shipment Delay
    # ---------------------------------------

    elif "delay" in query_lower:

        result = check_shipment_delay(
            shipment_id
        )

    # ---------------------------------------
    # Shipment Location
    # ---------------------------------------

    elif "location" in query_lower:

        result = get_shipment_location(
            shipment_id
        )

    # ---------------------------------------
    # Track Shipment
    # ---------------------------------------

    else:

        result = track_shipment(
            shipment_id
        )

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

Generate the final response.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state