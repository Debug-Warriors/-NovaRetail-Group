from graph.state import SupplyChainState


def route_request(state: SupplyChainState):

    intent = state.get(
        "intent",
        ""
    ).strip().lower()

    mapping = {

    "shipment":
        "shipment_agent",

    "inventory":
        "inventory_agent",

    "supplier":
        "supplier_agent",

    "incident":
        "incident_agent",

    "recovery":
        "recovery_agent",

    "reporting":
        "reporting_agent",

    "risk":
        "risk",

    "general":
        "general_agent",

    "unsupported":
        "unsupported",

    }

    return mapping.get(
        intent,
        "unsupported"
    )