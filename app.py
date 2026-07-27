import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from graph.workflow import graph

st.set_page_config(
    page_title="NovaRetail AI Assistant",
    page_icon="📦",
    layout="wide"
)

st.title("📦 NovaRetail Supply Chain Assistant")

st.markdown("""
Ask me about:

- 🚚 Shipment Tracking
- 📦 Inventory
- 🏭 Suppliers
- ⚠️ Incidents
- 🔄 Recovery Planning
""")

# ----------------------------
# Session State
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = {}

if "pending_state" not in st.session_state:
    st.session_state.pending_state = None

# ----------------------------
# Display Chat History
# ----------------------------

for message in st.session_state.messages:

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):
            st.markdown(message.content)

    else:

        with st.chat_message("assistant"):
            st.markdown(message.content)

# ----------------------------
# User Input
# ----------------------------

prompt = st.chat_input("Ask a supply chain question...")

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

    result = graph.invoke(state)

    st.session_state.memory = result["memory"]

    assistant_reply = result["response"]

    st.session_state.messages.append(
        AIMessage(content=assistant_reply)
    )

    with st.chat_message("assistant"):

        st.markdown(assistant_reply)

        with st.expander("Execution Details"):

            st.write("Intent:", result["intent"])
            st.write("Agent:", result["current_agent"])
            st.json(result["tool_result"])

    # --------------------------------
    # Approval Required?
    # --------------------------------

    if (
        "approval" in assistant_reply.lower()
        or "approve" in assistant_reply.lower()
    ):

        st.session_state.pending_state = result

# --------------------------------
# Approval Buttons
# --------------------------------

if st.session_state.pending_state is not None:

    st.divider()

    st.subheader("Human Approval Required")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Approve"):

            pending = st.session_state.pending_state

            pending["approval"] = True

            result = graph.invoke(pending)

            st.session_state.messages.append(
                AIMessage(content=result["response"])
            )

            st.session_state.memory = result["memory"]

            st.session_state.pending_state = None

            st.rerun()

    with col2:

        if st.button("❌ Reject"):

            st.session_state.messages.append(

                AIMessage(
                    content="Operation cancelled."
                )

            )

            st.session_state.pending_state = None

            st.rerun()