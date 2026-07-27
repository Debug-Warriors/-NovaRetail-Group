"""
Unsupported Agent

Handles requests outside the supply chain domain.
"""

from graph.state import SupplyChainState


def unsupported_agent(state: SupplyChainState):

    state["current_agent"] = "Unsupported Agent"

    state["tool_result"] = {}

    state["response"] = (
        "I can only assist with NovaRetail supply chain operations.\n\n"
        "Supported topics include:\n"
        "- Shipment Tracking\n"
        "- Inventory\n"
        "- Suppliers\n"
        "- Incidents\n"
        "- Recovery Planning\n"
        "- Reporting"
    )

    return state