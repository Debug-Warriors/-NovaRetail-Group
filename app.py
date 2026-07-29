import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from graph.workflow import graph

# ---------------------------------------------------
# Page Config (Must be first Streamlit command)
# ---------------------------------------------------

st.set_page_config(
    page_title="NovaRetail Supply Chain AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Page & Background */
.stApp {
    background: #f4f7fc;
}

.block-container {
    padding-top: 2rem;
}

/* Force Sidebar Styling */
section[data-testid="stSidebar"] {
    display: block !important;
    background-color: #17324d !important;
    min-width: 300px !important;
    max-width: 300px !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar Custom Button Styling to look like clickable list links */
section[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    color: #ffffff !important;
    border: none !important;
    text-align: left !important;
    padding: 6px 0px !important;
    font-size: 15px !important;
    width: 100% !important;
    box-shadow: none !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    color: #4da6ff !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

/* Main Header Styling */
.main-title {
    font-size: 38px;
    font-weight: 700;
    color: #1f4e79;
}

.sub-title {
    font-size: 16px;
    color: #666;
    margin-top: -6px;
}

/* Metric Cards */
.metric-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.metric-title {
    font-size: 15px;
    color: #666;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #1f4e79;
}

/* Chat Styling */
.stChatMessage {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Session State Initialization
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = {}

# Variable to hold click events from sidebar options
clicked_query = None

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:
    st.title("📦 NovaRetail")

    st.success("🟢 Ollama Connected")

    st.divider()

    st.subheader("Supported Operations")

    # Interactive links for supported operations
    if st.button("🚚  Shipment Tracking", use_container_width=True):
        clicked_query = "Show me current shipment tracking status."

    if st.button("📦  Inventory Management", use_container_width=True):
        clicked_query = "Give me an inventory status report."

    if st.button("🏭  Supplier Overview", use_container_width=True):
        clicked_query = "Show supplier details and performance overview."

    if st.button("⚠  Incident Resolution", use_container_width=True):
        clicked_query = "Are there any active supply chain incidents?"

    if st.button("🔄  Recovery Planning", use_container_width=True):
        clicked_query = "Generate a recovery plan for delayed shipments."

    if st.button("📊  Operations Reporting", use_container_width=True):
        clicked_query = "Provide an overall operations summary report."

    st.divider()

    st.subheader("Session Stats")

    st.metric("Messages", len(st.session_state.messages))
    st.metric("Memory Keys", len(st.session_state.memory))

    # Visual Capacity Bar
    max_messages = 50
    msg_count = len(st.session_state.messages)
    usage_ratio = min(msg_count / max_messages, 1.0)

    st.write("**Context Capacity**")
    st.progress(usage_ratio, text=f"{msg_count} / {max_messages} messages")

# ---------------------------------------------------
# Main Content - Header
# ---------------------------------------------------

st.markdown("""
<div class="main-title">
📦 NovaRetail Supply Chain AI
</div>

<div class="sub-title">
Enterprise Multi-Agent Supply Chain Operations Assistant
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🚚 Shipments</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">⚠ Delayed</div>
        <div class="metric-value">1</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">📦 Products</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">🏭 Suppliers</div>
        <div class="metric-value">3</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    elif isinstance(message, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(message.content)

# ---------------------------------------------------
# Chat Input & Processing
# ---------------------------------------------------

input_prompt = st.chat_input("Ask a supply chain question...")

# Determine if input came from the chat bar or a clicked link button
prompt = input_prompt or clicked_query

if prompt:

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    state = {
        "messages": st.session_state.messages,
        "user_query": prompt,
        "intent": "",
        "current_agent": "",
        "tool_result": {},
        "response": "",
        "approval": False,
        "memory": st.session_state.memory,
    }

    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):
            result = graph.invoke(state)

        reply = result["response"]

        st.markdown(reply)

        with st.expander("⚙ Execution Details"):

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Routing")
                st.write("**Intent**")
                st.info(result["intent"])

                st.write("**Agent**")
                st.success(result["current_agent"])

            with col2:
                st.markdown("### Context")

                st.write("**Memory Items**")
                st.write(len(result["memory"]))

                st.write("**Conversation Messages**")
                st.write(len(result["messages"]))

            st.divider()

            st.markdown("### Tool Output")

            if result["tool_result"]:
                st.json(result["tool_result"])
            else:
                st.info("No tool output.")

            st.divider()

            st.markdown("### Workflow")

            st.markdown(f"""
✅ Supervisor

⬇

✅ {result["current_agent"]}

⬇

✅ Tool Executed

⬇

✅ Response Generated
""")

    st.session_state.messages.append(
        AIMessage(content=reply)
    )

    st.session_state.memory = result["memory"]
    st.rerun()