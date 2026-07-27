"""
Inventory Agent

Responsibilities:
- Check product stock
- Detect shortages
- Check warehouse availability
"""

import re

from langchain_core.messages import SystemMessage, HumanMessage

from llm import llm
from graph.state import SupplyChainState

from tools.inventory_tools import (
    check_inventory,
    check_inventory_shortage,
    warehouse_availability,
    identify_inventory_shortage,
    load_inventory,
)

from utils.prompt_loader import load_prompt

INVENTORY_PROMPT = load_prompt("inventory.txt")


def extract_product_id(query: str):
    """
    Extract product IDs like:
    P100
    P200
    """

    match = re.search(r"P\d+", query.upper())

    if match:
        return match.group()

    return None


def extract_product_name(query: str):
    """
    Find a product by name.
    """

    inventory = load_inventory()

    query_lower = query.lower()

    for item in inventory:

        if item["product_name"].lower() in query_lower:
            return item["product_id"]

    return None


def extract_warehouse(query: str):
    """
    Extract warehouse from natural language.
    """

    warehouses = {
        "dallas": "Dallas Regional Warehouse",
        "new york": "New York Regional Warehouse",
        "chicago": "Chicago Regional Warehouse",
    }

    query_lower = query.lower()

    for key, value in warehouses.items():

        if key in query_lower:
            return value

    return None


def inventory_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Inventory Agent"

    query_lower = query.lower()

    # --------------------------------
    # Overall Inventory Shortage
    # --------------------------------

    if (
        "inventory shortage" in query_lower
        or "identify shortage" in query_lower
        or "identify inventory shortage" in query_lower
        or "low stock products" in query_lower
        or "all shortages" in query_lower
        or "products below minimum" in query_lower
    ):

        result = identify_inventory_shortage()

    # --------------------------------
    # Warehouse Availability
    # --------------------------------

    elif "warehouse" in query_lower:

        warehouse = extract_warehouse(query)

        if warehouse is None:
            warehouse = memory.get("last_warehouse")

        if warehouse is None:

            state["response"] = (
                "Please specify a warehouse.\n\n"
                "Examples:\n"
                "- Dallas warehouse\n"
                "- New York warehouse\n"
                "- Chicago warehouse"
            )

            return state

        memory["last_warehouse"] = warehouse

        result = warehouse_availability(warehouse)

    # --------------------------------
    # Product Lookup
    # --------------------------------

    else:

        product_id = extract_product_id(query)

        if product_id is None:
            product_id = extract_product_name(query)

        if product_id is None:
            product_id = memory.get("last_product")

        if product_id is None:

            state["response"] = (
                "Please provide a Product ID or Product Name.\n\n"
                "Examples:\n"
                "- P100\n"
                "- Wireless Headphones"
            )

            return state

        memory["last_product"] = product_id

        if (
            "shortage" in query_lower
            or "low stock" in query_lower
        ):

            result = check_inventory_shortage(product_id)

        else:

            result = check_inventory(product_id)

    state["tool_result"] = result

    messages = [

        SystemMessage(content=INVENTORY_PROMPT),

        HumanMessage(
            content=f"""
User Request:

{query}

Inventory Data:

{result}

Generate a helpful response.
"""
        ),
    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state