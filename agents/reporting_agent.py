from datetime import datetime

"""
Reporting Agent

Responsibilities:
- Incident summaries
- Operational reports
- Stakeholder communication
"""

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
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

    today = datetime.now().strftime("%d %B %Y")

    query_lower = query.lower()

    # --------------------------------------------------
    # Incident Summary
    # --------------------------------------------------

    if any(x in query_lower for x in [

        "incident summary",

        "incident report",

        "open incidents",

        "active incidents"

    ]):

        result = generate_incident_summary()

        report_title = "Incident Summary Report"

    # --------------------------------------------------
    # Stakeholder Update
    # --------------------------------------------------

    elif any(x in query_lower for x in [

        "stakeholder",

        "executive update",

        "leadership update",

        "notification",

        "business update"

    ]):

        if not state.get("approval", False):

            state["response"] = (
                "⚠️ Sending stakeholder updates requires approval.\n\n"
                "Please approve to continue."
            )

            state["tool_result"] = {}

            return state

        result = create_stakeholder_update()

        report_title = "Stakeholder Update"

    # --------------------------------------------------
    # Operational Report (Default)
    # --------------------------------------------------

    else:

        result = generate_operational_report()

        report_title = "NovaRetail Operations Report"

    state["tool_result"] = result

    messages = [

        SystemMessage(
            content=REPORTING_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}

Operational Data:

{result}

Generate ONLY the report body.

Start with:

Summary:

Then include, when appropriate:

- Key Findings
- Recommendations
- Next Steps

Use ONLY the supplied data.
Do not invent information.
"""
        )

    ]

    response = llm.invoke(messages)

    header = f"""# {report_title}

**Date:** {today}

"""

    state["response"] = header + response.content

    return state