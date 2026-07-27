"""
Recovery Agent

Responsibilities:
- Recommend recovery actions
- Compare alternatives
- Generate recovery plans

Human approval required before approving a recovery plan.
"""

import re

from langchain_core.messages import SystemMessage, HumanMessage

from llm import llm
from graph.state import SupplyChainState

from utils.prompt_loader import load_prompt

from tools.recovery_tools import (
    generate_recovery_plan,
)

RECOVERY_PROMPT = load_prompt("recovery.txt")


PRODUCTS = {
    "P100": "Wireless Headphones",
    "P200": "Smart Watches",
    "P300": "Laptop Accessories",
}


def extract_shipment_id(query: str):

    match = re.search(r"SHP\d+", query.upper())

    if match:
        return match.group()

    return None


def extract_product_id(query: str):

    match = re.search(r"P\d+", query.upper())

    if match:
        return match.group()

    return None


def recovery_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Recovery Agent"

    # -----------------------------
    # Human Approval
    # -----------------------------

    if not state.get("approval", False):

        state["response"] = (
            "⚠️ Recovery plans require approval.\n\n"
            "Approve the recovery plan to continue."
        )

        return state

    # -----------------------------
    # Shipment
    # -----------------------------

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

    # -----------------------------
    # Product
    # -----------------------------

    product_id = extract_product_id(query)

    if product_id is None:
        product_id = memory.get("last_product")

    if product_id is None:

        state["response"] = (
            "Please provide a Product ID.\n"
            "Example: P100"
        )

        return state

    memory["last_product"] = product_id

    product_name = PRODUCTS.get(product_id)

    if product_name is None:

        state["response"] = (
            "Unknown Product ID."
        )

        return state

    result = generate_recovery_plan(

        shipment_id,

        product_name,

        product_id

    )

    state["tool_result"] = result

    messages = [

        SystemMessage(
            content=RECOVERY_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Recovery Information:

{result}

Generate a recovery recommendation.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state