"""
Supplier Agent

Responsibilities:
- Find supplier details
- Check supplier availability
- Find alternative suppliers
"""

import re

from langchain_core.messages import SystemMessage, HumanMessage

from llm import llm
from graph.state import SupplyChainState

from tools.supplier_tools import (
    find_supplier,
    check_supplier_availability,
    find_alternative_suppliers,
)

from utils.prompt_loader import load_prompt

SUPPLIER_PROMPT = load_prompt("supplier.txt")


def extract_supplier_name(query: str):
    """
    Extract supplier name.

    Example:
        Find supplier ABC Electronics

    Returns:
        ABC Electronics
    """

    match = re.search(
        r"supplier\s+(.+)",
        query,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).strip()

    return None


def inventory_products():
    """
    Product list used for matching.
    """

    return [
        "Wireless Headphones",
        "Smart Watches",
        "Laptop Accessories",
        "Tablets",
    ]


def extract_product(query: str):
    """
    Extract product name from query.
    """

    query_lower = query.lower()

    for product in inventory_products():

        if product.lower() in query_lower:
            return product

    return None


def supplier_agent(state: SupplyChainState):

    query = state["user_query"]

    memory = state.setdefault("memory", {})

    query_lower = query.lower()

    state["current_agent"] = "Supplier Agent"

    # -----------------------------------
    # Alternative Supplier
    # -----------------------------------

    if (
        "alternative" in query_lower
        or "another supplier" in query_lower
        or "replacement supplier" in query_lower
    ):

        product = extract_product(query)

        if product is None:
            product = memory.get("last_product")

        if product is None:

            state["response"] = (
                "Please specify the product name."
            )

            return state

        memory["last_product"] = product

        # -----------------------------------
        # Human Approval Required
        # -----------------------------------

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Selecting an alternative supplier requires approval.\n\n"
                "Press 'Approve' to continue."
            )

            state["tool_result"] = {}

            state["memory"] = memory

            return state

        result = find_alternative_suppliers(product)

    # -----------------------------------
    # Supplier Availability
    # -----------------------------------

    elif "availability" in query_lower:

        supplier = extract_supplier_name(query)

        if supplier is None:
            supplier = memory.get("last_supplier")

        if supplier is None:

            state["response"] = (
                "Please specify the supplier name."
            )

            return state

        memory["last_supplier"] = supplier

        result = check_supplier_availability(
            supplier
        )

    # -----------------------------------
    # Supplier Details
    # -----------------------------------

    else:

        supplier = extract_supplier_name(query)

        if supplier is None:
            supplier = memory.get("last_supplier")

        if supplier is None:

            state["response"] = (
                "Please specify the supplier name."
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

Generate the final answer.
"""
        ),
    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    state["memory"] = memory

    return state