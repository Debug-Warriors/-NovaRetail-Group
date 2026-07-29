"""
NovaRetail Supply Chain LangGraph Workflow

Architecture:

User
 |
 v
Supervisor Agent
 |
 v
Router
 |
 +--> Shipment Agent
 |
 +--> Inventory Agent
 |
 +--> Supplier Agent
 |
 +--> Incident Agent
 |
 +--> Recovery Agent
 |
 +--> Reporting Agent
 |
 v
Final Response
"""
from agents.general_agent import general_agent


from langgraph.graph import (
    StateGraph,
    START,
    END
)


from graph.state import SupplyChainState

from graph.router import route_request


# Agents

from agents.supervisor import supervisor_agent

from agents.shipment_agent import shipment_agent

from agents.inventory_agent import inventory_agent

from agents.supplier_agent import supplier_agent

from agents.incident_agent import incident_agent

from agents.recovery_agent import recovery_agent

from agents.reporting_agent import reporting_agent
from agents.unsupported_agent import unsupported_agent
from agents.risk_agent import risk_agent


# ------------------------------------------------
# Create Graph
# ------------------------------------------------

builder = StateGraph(
    SupplyChainState
)



# ------------------------------------------------
# Register Nodes
# ------------------------------------------------

builder.add_node(
    "general_agent",
    general_agent
)

builder.add_node(
    "supervisor",
    supervisor_agent
)


builder.add_node(
    "shipment_agent",
    shipment_agent
)


builder.add_node(
    "inventory_agent",
    inventory_agent
)


builder.add_node(
    "supplier_agent",
    supplier_agent
)


builder.add_node(
    "incident_agent",
    incident_agent
)


builder.add_node(
    "recovery_agent",
    recovery_agent
)


builder.add_node(
    "reporting_agent",
    reporting_agent
)
builder.add_node(
    "unsupported",
    unsupported_agent
)

builder.add_node(
    "risk", 
    risk_agent
)

# ------------------------------------------------
# Starting Point
# ------------------------------------------------

builder.add_edge(
    START,
    "supervisor"
)

builder.add_edge(
    "general_agent",
    END
)



# ------------------------------------------------
# Supervisor Routing
# ------------------------------------------------

builder.add_conditional_edges(

    "supervisor",

    route_request,

    {

        "shipment_agent":
            "shipment_agent",

        "inventory_agent":
            "inventory_agent",

        "supplier_agent":
            "supplier_agent",

        "incident_agent":
            "incident_agent",

        "recovery_agent":
            "recovery_agent",

        "reporting_agent":
            "reporting_agent",
        "unsupported":
            "unsupported",
        "risk": 
            "risk",
        "general_agent":
            "general_agent",

    }

)



# ------------------------------------------------
# End Connections
# ------------------------------------------------

builder.add_edge(
    "shipment_agent",
    END
)


builder.add_edge(
    "inventory_agent",
    END
)


builder.add_edge(
    "supplier_agent",
    END
)


builder.add_edge(
    "incident_agent",
    END
)


builder.add_edge(
    "recovery_agent",
    END
)


builder.add_edge(
    "reporting_agent",
    END
)
builder.add_edge(
    "unsupported",
    END
)
builder.add_edge(
    "risk", 
    END
)


# ------------------------------------------------
# Compile Application Graph
# ------------------------------------------------

graph = builder.compile()