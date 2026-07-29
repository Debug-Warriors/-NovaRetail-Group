"""
Inventory Agent

Responsibilities:
- Check product inventory
- Detect shortages
- Check warehouse inventory
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

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


# -------------------------------------------------------
# Extract Product ID
# -------------------------------------------------------

def extract_product_id(query: str):

    match = re.search(r"P\d+", query.upper())

    if match:
        return match.group()

    return None


# -------------------------------------------------------
# Extract Product Name
# -------------------------------------------------------

def extract_product_name(query: str):

    inventory = load_inventory()

    query_lower = query.lower()

    for item in inventory:

        if item["product_name"].lower() in query_lower:

            return item["product_id"]

    return None


# -------------------------------------------------------
# Extract Warehouse ID
# -------------------------------------------------------

def extract_warehouse(query: str):

    match = re.search(r"W\d+", query.upper())

    if match:
        return match.group()

    warehouse_map = {

        "dallas": "W001",

        "new york": "W002",

        "chicago": "W003",

        "phoenix": "W004",

        "miami": "W005",

        "boston": "W006",

        "los angeles": "W007",

        "seattle": "W008",

        "san francisco": "W009",

        "denver": "W010"

    }

    q = query.lower()

    for city, wid in warehouse_map.items():

        if city in q:

            return wid

    return None


# -------------------------------------------------------
# Inventory Agent
# -------------------------------------------------------

def inventory_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    state["current_agent"] = "Inventory Agent"

    query_lower = query.lower()

    # --------------------------------------------------
    # Inventory Shortages
    # --------------------------------------------------

    if any(x in query_lower for x in [

        "inventory shortage",

        "identify shortage",

        "identify inventory shortage",

        "low stock products",

        "all shortages",

        "products below minimum"

    ]):

        result = identify_inventory_shortage()

    # --------------------------------------------------
    # Warehouse Query
    # --------------------------------------------------

    elif "warehouse" in query_lower:

        warehouse = extract_warehouse(query)

        if warehouse is None:

            warehouse = memory.get("last_warehouse")

        if warehouse is None:

            state["response"] = (
                "Please provide a Warehouse ID (W001-W010) "
                "or warehouse city."
            )

            return state

        memory["last_warehouse"] = warehouse

        result = warehouse_availability(warehouse)

    # --------------------------------------------------
    # Product Query
    # --------------------------------------------------

    else:

        product_id = extract_product_id(query)

        if product_id is None:

            product_id = extract_product_name(query)

        if product_id is None:

            product_id = memory.get("last_product")

        if product_id is None:

            state["response"] = (
                "Please provide a Product ID (P100-P119) "
                "or product name."
            )

            return state

        memory["last_product"] = product_id

        if (

            "shortage" in query_lower

            or

            "low stock" in query_lower

        ):

            result = check_inventory_shortage(product_id)

        else:

            result = check_inventory(product_id)

    # --------------------------------------------------
    # Save Tool Result
    # --------------------------------------------------

    state["tool_result"] = result

    # --------------------------------------------------
    # LLM Response
    # --------------------------------------------------

    messages = [

        SystemMessage(content=INVENTORY_PROMPT),

        HumanMessage(
            content=f"""
User Request:

{query}

Inventory Data:

{result}

Generate a professional inventory response.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state