"""
Supplier Agent

Responsibilities:
- Find supplier details
- Check supplier availability
- Find alternative suppliers
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from llm import llm

from graph.state import SupplyChainState

from tools.supplier_tools import (
    find_supplier,
    check_supplier_availability,
    find_alternative_suppliers,
)

from tools.inventory_tools import load_inventory

from utils.prompt_loader import load_prompt

SUPPLIER_PROMPT = load_prompt("supplier.txt")


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def extract_supplier_name(query: str):

    match = re.search(
        r"supplier\s+(.+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).strip()

    return None


def extract_product_id(query: str):

    match = re.search(r"P\d+", query.upper())

    if match:
        return match.group()

    return None


def extract_product_name(query: str):

    inventory = load_inventory()

    query_lower = query.lower()

    for item in inventory:

        if item["product_name"].lower() in query_lower:

            return item["product_name"]

    return None


# -------------------------------------------------------
# Supplier Agent
# -------------------------------------------------------

def supplier_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    query_lower = query.lower()

    state["current_agent"] = "Supplier Agent"

    # --------------------------------------------------
    # Alternative Suppliers
    # --------------------------------------------------

    if any(x in query_lower for x in [

        "alternative",

        "replacement",

        "another supplier",

        "backup supplier"

    ]):

        product = extract_product_name(query)

        if product is None:

            product_id = extract_product_id(query)

            if product_id:

                inventory = load_inventory()

                for item in inventory:

                    if item["product_id"] == product_id:

                        product = item["product_name"]

                        break

        if product is None:

            product = memory.get("last_product")

        if product is None:

            state["response"] = (
                "Please provide a Product ID or Product Name."
            )

            return state

        memory["last_product"] = product

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Selecting an alternative supplier requires approval.\n\n"
                "Please approve to continue."
            )

            state["tool_result"] = {}

            state["memory"] = memory

            return state

        result = find_alternative_suppliers(product)

    # --------------------------------------------------
    # Supplier Availability
    # --------------------------------------------------

    elif any(x in query_lower for x in [

        "availability",

        "available",

        "can supply"

    ]):

        supplier = extract_supplier_name(query)

        if supplier is None:

            supplier = memory.get("last_supplier")

        if supplier is None:

            state["response"] = (
                "Please provide the supplier name."
            )

            return state

        memory["last_supplier"] = supplier

        result = check_supplier_availability(supplier)

    # --------------------------------------------------
    # Supplier Details
    # --------------------------------------------------

    else:

        supplier = extract_supplier_name(query)

        if supplier is None:

            supplier = memory.get("last_supplier")

        if supplier is None:

            state["response"] = (
                "Please provide the supplier name."
            )

            return state

        memory["last_supplier"] = supplier

        result = find_supplier(supplier)

    state["tool_result"] = result

    messages = [

        SystemMessage(
            content=SUPPLIER_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Supplier Data:

{result}

Generate a professional supplier response.

Use only the supplied supplier information.
Do not invent details.
"""
        ),

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state