"""
Reporting Agent

Responsibilities:
- Incident summaries
- Operational reports
- Stakeholder communication
"""

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from llm import llm

from graph.state import SupplyChainState

from utils.prompt_loader import load_prompt

from tools.reporting_tools import (
    generate_incident_summary,
    generate_operational_report,
    create_stakeholder_update,
)

REPORTING_PROMPT = load_prompt("reporting.txt")


def reporting_agent(state: SupplyChainState):

    query = state["user_query"]

    state["current_agent"] = "Reporting Agent"

    query_lower = query.lower()

    # ------------------------------------
    # Incident Summary
    # ------------------------------------

    if "incident summary" in query_lower:

        result = generate_incident_summary()

    # ------------------------------------
    # Operational Report
    # ------------------------------------

    elif "report" in query_lower:

        result = generate_operational_report()

    # ------------------------------------
    # Stakeholder Update
    # ------------------------------------

    elif (
        "stakeholder" in query_lower
        or "update" in query_lower
        or "notification" in query_lower
    ):

        # Human approval required

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Sending stakeholder notifications requires approval.\n\n"
                "Press 'Approve' to continue."
            )

            state["tool_result"] = {}

            return state

        result = create_stakeholder_update()

    # ------------------------------------
    # Default
    # ------------------------------------

    else:

        result = generate_operational_report()

    state["tool_result"] = result

    messages = [

        SystemMessage(
            content=REPORTING_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Report Data:

{result}

Generate the final response.
"""
        )

    ]

    response = llm.invoke(messages)

    state["response"] = response.content

    return state