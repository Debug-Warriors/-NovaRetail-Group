"""
Incident Agent

Responsibilities:
- Create Incident
- Check Incident Status
- Escalate Incident

Human approval is required before creating an incident.
"""

import re

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from graph.state import SupplyChainState
from llm import llm

from utils.prompt_loader import load_prompt

from tools.incident_tools import (
    create_incident,
    get_incident,
    escalate_incident,
)

PROMPT = load_prompt("incident.txt")


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def extract_incident_id(query: str):

    match = re.search(r"INC\d+", query.upper())

    if match:
        return match.group()

    return None


def extract_shipment_id(query: str):

    match = re.search(r"SHP\d+", query.upper())

    if match:
        return match.group()

    return ""


# -------------------------------------------------------
# Agent
# -------------------------------------------------------

def incident_agent(state: SupplyChainState):

    query = state["user_query"]

    state["current_agent"] = "Incident Agent"

    query_lower = query.lower()

    # --------------------------------------------------
    # Incident Status
    # --------------------------------------------------

    if "status" in query_lower:

        incident_id = extract_incident_id(query)

        if incident_id is None:

            state["response"] = "Please provide an Incident ID."

            return state

        result = get_incident(incident_id)

        state["tool_result"] = result

    # --------------------------------------------------
    # Escalate
    # --------------------------------------------------

    elif "escalate" in query_lower:

        incident_id = extract_incident_id(query)

        if incident_id is None:

            state["response"] = "Please provide an Incident ID."

            return state

        result = escalate_incident(incident_id)

        state["tool_result"] = result

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    else:

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Creating an incident requires approval.\n\n"
                "Press 'Approve' to continue."
            )

            state["tool_result"] = {}

            return state

        shipment_id = extract_shipment_id(query)

        incident = create_incident(

            shipment_id=shipment_id,

            order_id="",

            supplier_id="",

            warehouse_id="",

            product_id="",

            category="General",

            severity="High",

            root_cause="Under Investigation",

            impact=query,

            assigned_team="Operations",

            risk_score=75

        )

        state["tool_result"] = incident

    # --------------------------------------------------
    # LLM Response
    # --------------------------------------------------

    messages = [

        SystemMessage(content=PROMPT),

        HumanMessage(
            content=f"""
User Request:

{query}

Incident Data:

{state['tool_result']}

Generate a professional response for NovaRetail.
"""
        ),
    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    return state