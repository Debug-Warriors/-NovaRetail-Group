"""
Incident Agent

Responsibilities:
- Create Incident
- Check Incident Status
- Escalate Incident

Human approval is required before creating an incident.
"""

import re

from langchain_core.messages import SystemMessage, HumanMessage

from graph.state import SupplyChainState
from llm import llm

from utils.prompt_loader import load_prompt

from tools.incident_tools import (
    create_incident,
    get_incident,
    escalate_incident,
)

PROMPT = load_prompt("incident.txt")


def extract_incident_id(query: str):

    """
    Extract incident IDs like:
    INC12345
    A1B2C3D4
    """

    match = re.search(r"[A-Z0-9]{8}", query.upper())

    if match:
        return match.group()

    return None


def incident_agent(state: SupplyChainState):

    query = state["user_query"]

    state["current_agent"] = "Incident Agent"

    query_lower = query.lower()

    # ------------------------------------------
    # Check incident status
    # ------------------------------------------

    if "status" in query_lower:

        incident_id = extract_incident_id(query)

        if incident_id is None:

            state["response"] = (
                "Please provide an Incident ID."
            )

            return state

        result = get_incident(incident_id)

        state["tool_result"] = result

    # ------------------------------------------
    # Escalate Incident
    # ------------------------------------------

    elif "escalate" in query_lower:

        incident_id = extract_incident_id(query)

        if incident_id is None:

            state["response"] = (
                "Please provide an Incident ID."
            )

            return state

        result = escalate_incident(incident_id)

        state["tool_result"] = result

    # ------------------------------------------
    # Create Incident
    # ------------------------------------------

    else:

        # Human approval required

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Creating an incident requires approval.\n\n"
                "Press 'Approve' to continue."
            )

            state["tool_result"] = {}

            return state

        incident = create_incident(
            title="Supply Chain Incident",
            description=query,
            severity="High"
        )

        state["tool_result"] = incident

    # ------------------------------------------
    # Generate response using Llama
    # ------------------------------------------

    messages = [

        SystemMessage(content=PROMPT),

        HumanMessage(
            content=f"""
User Request:

{query}

Incident Data:

{state['tool_result']}

Generate the final response.
"""
        ),
    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    return state