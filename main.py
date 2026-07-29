"""
NovaRetail CrisisOps AI
Phase 2 - Predictive Supply Chain Risk Intelligence

Enterprise Streamlit Dashboard
"""

from datetime import datetime
import json

import streamlit as st

from graph.workflow import graph


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NovaRetail CrisisOps AI",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

section[data-testid="stSidebar"]{
    width:320px !important;
    min-width:320px !important;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

.title-card{
    background:#2563EB;
    color:white;
    padding:25px;
    border-radius:12px;
    margin-bottom:20px;
}

.metric-card{
    background:#F8FAFC;
    border:1px solid #E5E7EB;
    border-radius:10px;
    padding:15px;
}

.chat-card{
    background:#F9FAFB;
    border-radius:10px;
    padding:15px;
    border:1px solid #E5E7EB;
}

.footer-card{
    background:#F3F4F6;
    border-radius:10px;
    padding:15px;
}

.success-card{
    background:#ECFDF5;
    border-left:6px solid #10B981;
    padding:15px;
    border-radius:8px;
}

.warning-card{
    background:#FEF3C7;
    border-left:6px solid #F59E0B;
    padding:15px;
    border-radius:8px;
}

.danger-card{
    background:#FEF2F2;
    border-left:6px solid #EF4444;
    padding:15px;
    border-radius:8px;
}

.info-card{
    background:#EFF6FF;
    border-left:6px solid #3B82F6;
    padding:15px;
    border-radius:8px;
}

.small-text{
    font-size:13px;
    color:gray;
}

</style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph_state" not in st.session_state:
    st.session_state.graph_state = {}

if "approval" not in st.session_state:
    st.session_state.approval = False

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "🏠 Dashboard"

if "memory" not in st.session_state:
    st.session_state.memory = {}

# ==========================================================
# HELPER FUNCTIONS
# ==========================================================


def risk_color(level: str):
    level = str(level).lower()
    if level == "critical":
        return "🔴"
    if level == "high":
        return "🟠"
    if level == "medium":
        return "🟡"
    return "🟢"


def pretty_json(data):
    try:
        return json.dumps(data, indent=4)
    except Exception:
        return str(data)


def execute_graph(user_query: str):
    state = {
        "user_query": user_query,
        "approval": st.session_state.approval,
        "memory": st.session_state.memory,
    }

    result = graph.invoke(state)
    st.session_state.graph_state = result
    st.session_state.memory = result.get("memory", {})
    return result


def add_chat(role, message):
    st.session_state.messages.append(
        {
            "role": role,
            "content": message,
        }
    )


def clear_chat():
    st.session_state.messages = []
    st.session_state.graph_state = {}
    st.session_state.approval = False
    st.session_state.pending_query = None


# ==========================================================
# TOP RIGHT ACTIONS
# ==========================================================

top1, top2, top3 = st.columns([8, 1, 1])

with top2:
    if st.button("🧹 Clear"):
        clear_chat()
        st.rerun()

with top3:
    if st.button("🔄 Refresh"):
        st.rerun()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding-bottom:20px;'>
            <h1 style='color:#2563EB;'>NovaRetail</h1>
            <p style='color:gray;'>CrisisOps AI v2.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("## Navigation")

    st.session_state.selected_module = st.radio(
        "Select Module",
        [
            "🏠 Dashboard",
            "📦 Shipment",
            "📦 Inventory",
            "🏢 Suppliers",
            "⚠ Incidents",
            "🔄 Recovery",
            "📊 Reporting",
            "🧠 Risk Intelligence",
        ],
        key="navigation_radio",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("## Suggested Queries")

    suggestions = [
        "Track shipment SHP101",
        "Check inventory for P100",
        "Show supplier ABC Electronics",
        "Create incident for SHP108",
        "Generate operational report",
        "Predict supply chain risks",
        "Show warehouse risks",
        "Show high-risk suppliers",
    ]

    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.user_input = suggestion

    st.divider()

    st.markdown("### System")

    st.success("🟢 Operational")

    st.caption(
        f"Current Time\n\n{datetime.now().strftime('%d %B %Y %H:%M')}"
    )


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class='title-card'>
        <h1>🚚 NovaRetail CrisisOps AI</h1>
        <p>
        Multi-Agent Supply Chain Intelligence Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("System Status", "Operational")

with col2:
    risk = st.session_state.graph_state.get("overall_risk", "Low")
    st.metric("Overall Risk", risk)

with col3:
    score = st.session_state.graph_state.get("risk_score", 0)
    st.metric("Risk Score", score)

with col4:
    confidence = st.session_state.graph_state.get("confidence", 0)
    st.metric("Confidence", f"{confidence}%")

st.divider()


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.selected_module == "🏠 Dashboard":
    left, right = st.columns([2, 1])

    with left:
        st.subheader("Executive Dashboard")
        st.info(
            """
            CrisisOps AI continuously monitors shipments,
            suppliers, inventory, warehouses,
            operational incidents and predictive risks.
            """
        )

        st.write("")
        st.markdown("### Platform Capabilities")

        capabilities = [
            "Shipment Tracking",
            "Inventory Management",
            "Supplier Intelligence",
            "Incident Management",
            "Recovery Planning",
            "Executive Reporting",
            "Predictive Risk Intelligence",
        ]

        for capability in capabilities:
            st.success(f"✔ {capability}")

    with right:
        st.subheader("Platform Health")
        st.progress(100)
        st.success("System Operational")
        st.write("")

        st.metric("Active Agents", "7")
        st.metric("LLM", "Ollama")
        st.metric("Workflow", "LangGraph")
        st.metric("Risk Engine", "Enabled")

st.divider()


# ============================================================
# CHAT INTERFACE
# ============================================================

st.subheader("💬 CrisisOps AI Assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process input from sidebar suggestions or standard chat input
default_prompt = ""
if st.session_state.user_input:
    default_prompt = st.session_state.user_input
    st.session_state.user_input = ""

prompt = st.chat_input("Ask a supply chain question...")

if default_prompt:
    prompt = default_prompt

# ============================================================
# GRAPH EXECUTION (USER INPUT)
# ============================================================

if prompt:
    # Save the query for human-in-the-loop approval re-runs
    st.session_state.pending_query = prompt
    st.session_state.approval = False

    add_chat("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing request..."):
            result = execute_graph(prompt)
            response = result.get("response", "No response generated.")
            st.markdown(response)

    add_chat("assistant", response)


# ============================================================
# HUMAN-IN-THE-LOOP APPROVAL LOGIC
# ============================================================

graph_state = st.session_state.graph_state
response = graph_state.get("response", "")

# Evaluates state flag first, with string fallback for any approval-requiring agent
approval_required = (
    graph_state.get("approval_required", False)
    or "requires approval" in response.lower()
    or "press 'approve'" in response.lower()
) and not st.session_state.approval

if approval_required:
    st.divider()
    st.warning(
        "⚠️ High-impact or risk disruption action detected.\n"
        "Approval is required before this action can be executed."
    )

    c1, c2 = st.columns(2)

    with c1:
        if st.button("✅ Approve", use_container_width=True, type="primary"):
            st.session_state.approval = True

            # Re-run graph using the saved original prompt
            if st.session_state.pending_query:
                with st.spinner("Executing approved action..."):
                    result = execute_graph(st.session_state.pending_query)
                    approved_response = result.get(
                        "response", "Action completed."
                    )
                    add_chat("assistant", approved_response)

            st.rerun()

    with c2:
        if st.button("❌ Reject", use_container_width=True):
            st.session_state.approval = False
            st.session_state.pending_query = None
            st.info("Action cancelled by user.")


# ============================================================
# TOOL OUTPUT EXPANDER
# ============================================================

if graph_state.get("tool_result"):
    st.divider()
    with st.expander("🔍 Tool Output", expanded=False):
        st.code(pretty_json(graph_state["tool_result"]), language="json")


# ============================================================
# AGENT DETAILS & STATUS
# ============================================================

if graph_state:
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Agent", graph_state.get("current_agent", "-"))

    with col2:
        st.metric("Intent", graph_state.get("intent", "-").title())

    with col3:
        st.metric(
            "Approval",
            "Granted" if st.session_state.approval else "Not Required",
        )


# ============================================================
# RISK INTELLIGENCE DASHBOARD
# ============================================================

if graph_state.get("tool_result"):
    tool_result = graph_state["tool_result"]

    if isinstance(tool_result, dict) and "overall_risk" in tool_result:
        st.divider()
        st.header("🧠 Predictive Risk Intelligence")

        risk = tool_result.get("overall_risk", "Low")
        score = tool_result.get("risk_score", 0)
        confidence = tool_result.get("confidence", 0)
        total = tool_result.get("total_risks", 0)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Overall Risk", f"{risk_color(risk)} {risk}")

        with c2:
            st.metric("Risk Score", f"{score}/100")

        with c3:
            st.metric("Confidence", f"{confidence}%")

        with c4:
            st.metric("Detected Risks", total)

        st.write("")
        st.subheader("Confidence")
        st.progress(confidence / 100)
        st.write("")

        # ---------------------------------------------
        # Risk Table
        # ---------------------------------------------
        risks = tool_result.get("risks", [])

        if risks:
            st.subheader("Detected Risks")
            table = []
            for r in risks:
                table.append(
                    {
                        "Type": r.get("type"),
                        "Score": r.get("risk_score"),
                        "Confidence": f"{r.get('confidence')}%",
                        "Recommendation": r.get("recommendation", "-"),
                    }
                )

            st.dataframe(
                table, use_container_width=True, hide_index=True
            )

        # ---------------------------------------------
        # Individual Risks
        # ---------------------------------------------
        st.write("")
        st.subheader("Risk Details")

        for index, risk_item in enumerate(risks):
            with st.expander(
                f"{risk_color(risk_item['type'])} {risk_item['type']} Risk",
                expanded=False,
            ):
                st.markdown(
                    f"""
**Risk Score**

{risk_item["risk_score"]}

**Confidence**

{risk_item["confidence"]}%

**Recommendation**

{risk_item["recommendation"]}
"""
                )

                reasons = risk_item.get("reasons", [])
                if reasons:
                    st.markdown("### Why was this detected?")
                    for reason in reasons:
                        st.write(f"• {reason}")

        # ---------------------------------------------
        # Recommendations
        # ---------------------------------------------
        st.write("")
        st.subheader("Recommended Actions")

        recommendations = []
        for r in risks:
            recommendations.append(r["recommendation"])

        recommendations = sorted(list(set(recommendations)))

        for recommendation in recommendations:
            st.success(f"✔ {recommendation}")


# ============================================================
# FOOTER
# ============================================================

st.divider()

footer_left, footer_middle, footer_right = st.columns(3)

with footer_left:
    st.caption("Version\n\nCrisisOps AI v2.0")

with footer_middle:
    st.caption(
        f"Current Time\n\n{datetime.now().strftime('%d %B %Y %H:%M')}"
    )

with footer_right:
    st.caption("Powered by\n\nLangGraph • Ollama • Streamlit")

st.write("")
st.caption(
    "© 2026 NovaRetail CrisisOps AI | Predictive Supply Chain Risk Intelligence"
)