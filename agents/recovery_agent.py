"""
Recovery Agent

Responsibilities:
- Recommend recovery actions
- Generate recovery plans
- Suggest alternative suppliers

Human approval required before executing recovery planning.
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from llm import llm
from graph.state import SupplyChainState

from utils.prompt_loader import load_prompt

from tools.recovery_tools import (
    generate_recovery_plan,
    business_continuity_plan,
)

RECOVERY_PROMPT = load_prompt("recovery.txt")


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

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


# -------------------------------------------------------
# Recovery Agent
# -------------------------------------------------------

def recovery_agent(state: dict):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Recovery Agent"

    # --------------------------------------------------
    # Approval Required
    # --------------------------------------------------

    if not state.get("approval", False):

        state["response"] = (
            "⚠️ Recovery planning requires approval.\n\n"
            "Please approve before generating a recovery plan."
        )

        return state

    # --------------------------------------------------
    # Shipment
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Product
    # --------------------------------------------------

    product_id = extract_product_id(query)

    if product_id is None:

        product_id = memory.get("last_product")

    if product_id is None:

        state["response"] = (
            "Please provide a Product ID.\n\n"
            "Example: P100"
        )

        return state

    memory["last_product"] = product_id

    # --------------------------------------------------
    # Generate Recovery Plan
    # --------------------------------------------------

    if (
        "continuity" in query.lower()
        or
        "business continuity" in query.lower()
    ):

        result = business_continuity_plan(

            shipment_id,

            product_id

        )

    else:

        result = generate_recovery_plan(

            shipment_id,

            product_id

        )

    state["tool_result"] = result

    # --------------------------------------------------
    # LLM Response
    # --------------------------------------------------

    messages = [

        SystemMessage(
            content=RECOVERY_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Recovery Data:

{result}

Generate a professional recovery recommendation.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state