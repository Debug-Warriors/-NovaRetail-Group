"""
Risk Intelligence Agent

Phase 2 - Predictive Supply Chain Intelligence

Responsibilities
----------------
- Analyze operational risks
- Predict future disruptions
- Explain why risks exist
- Recommend preventive actions
- Provide confidence scores
"""

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from llm import llm

from graph.state import SupplyChainState

from utils.prompt_loader import load_prompt

from tools.risk_tools import (
    calculate_overall_risk,
)

RISK_PROMPT = load_prompt("risk.txt")


def risk_agent(state: SupplyChainState):

    query = state["user_query"]

    state["current_agent"] = "Risk Intelligence Agent"

    # -----------------------------------------
    # Run predictive analysis
    # -----------------------------------------

    risk_result = calculate_overall_risk()

    state["tool_result"] = risk_result

    # Store values in state

    state["risk_score"] = risk_result["risk_score"]

    state["confidence"] = risk_result["confidence"]

    # -----------------------------------------
    # Human approval
    # -----------------------------------------

    if (
        risk_result["overall_risk"] in ["High", "Critical"]
        and
        not state.get("approval", False)
    ):

        state["response"] = (
            "⚠️ High-risk supply chain disruption detected.\n\n"
            f"Overall Risk : {risk_result['overall_risk']}\n"
            f"Risk Score   : {risk_result['risk_score']}\n"
            f"Confidence   : {risk_result['confidence']}%\n\n"
            "Preventive actions have been generated.\n\n"
            "Press **Approve** to continue."
        )

        return state

    # -----------------------------------------
    # Build prompt
    # -----------------------------------------

    messages = [

        SystemMessage(
            content=RISK_PROMPT
        ),

        HumanMessage(
            content=f"""
User Request:

{query}


Risk Analysis:

{risk_result}


Generate:

1. Executive Summary

2. Overall Risk Level

3. Confidence Score

4. Top Risks

5. Business Impact

6. Recommended Preventive Actions

7. Explain WHY each risk was identified.

Use ONLY the supplied information.
"""
        )

    ]

    response = llm.invoke(messages)

    # -----------------------------------------
    # Save response
    # -----------------------------------------

    state["response"] = response.content

    return state