"""
Unsupported Agent

Handles requests outside the NovaRetail supply chain domain.
"""

from graph.state import SupplyChainState


def unsupported_agent(state: SupplyChainState):

    state["current_agent"] = "Unsupported Agent"

    state["tool_result"] = {}

    state["response"] = (
        "I can only assist with NovaRetail supply chain operations.\n\n"
        "Supported capabilities include:\n\n"
        "• Shipment Tracking\n"
        "• Inventory Management\n"
        "• Supplier Management\n"
        "• Incident Management\n"
        "• Recovery Planning\n"
        "• Operational Reporting\n"
        "• Risk Intelligence & Predictive Risk Analysis\n\n"
        "Example requests:\n"
        "- Track shipment SHP120\n"
        "- Check inventory for P119\n"
        "- Find supplier Core Industrial\n"
        "- Show high-risk suppliers\n"
        "- Generate an operational report\n"
        "- Assess overall supply chain risk"
    )

    return state