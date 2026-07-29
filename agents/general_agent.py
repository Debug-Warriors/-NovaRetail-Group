"""
General Agent

Handles:
- Greetings
- About the assistant
- Help
- Thanks
- Farewell
"""

from graph.state import SupplyChainState


def general_agent(state: SupplyChainState):

    query = state["user_query"].lower().strip()

    state["current_agent"] = "General Agent"

    state["tool_result"] = {}

    # -----------------------------
    # Greeting
    # -----------------------------

    if query in {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    }:

        state["response"] = (
            "👋 Hello! Welcome to CrisisOps AI.\n\n"
            "I'm NovaRetail's Predictive Supply Chain Risk Intelligence Assistant.\n\n"
            "How can I assist you today?"
        )

        return state

    # -----------------------------
    # About
    # -----------------------------

    if query in {
        "who are you",
        "who are you?",
        "what are you",
        "what are you?",
        "introduce yourself",
    }:

        state["response"] = (
            "I'm CrisisOps AI.\n\n"
            "I help NovaRetail monitor shipments, inventory, suppliers, incidents, "
            "recovery planning, operational reporting, and predictive supply chain risk."
        )

        return state

    # -----------------------------
    # Help
    # -----------------------------

    if query in {
        "help",
        "what can you do",
        "capabilities",
        "features",
    }:

        state["response"] = (
            "I can help with:\n\n"
            "📦 Shipment Tracking\n"
            "📦 Inventory Management\n"
            "🏢 Supplier Management\n"
            "⚠ Incident Management\n"
            "🔄 Recovery Planning\n"
            "📊 Operational Reporting\n"
            "🧠 Predictive Risk Intelligence\n\n"

            "Example requests:\n\n"

            "• Track shipment SHP120\n"
            "• Check inventory for P119\n"
            "• Find supplier Core Industrial\n"
            "• Generate recovery plan for SHP120 P119\n"
            "• Generate operational report\n"
            "• Assess overall supply chain risk"
        )

        return state

    # -----------------------------
    # Thanks
    # -----------------------------

    if query in {
        "thanks",
        "thank you",
        "thanks!",
    }:

        state["response"] = (
            "You're welcome! Let me know if you need any assistance with your supply chain operations."
        )

        return state

    # -----------------------------
    # Farewell
    # -----------------------------

    if query in {
        "bye",
        "goodbye",
        "see you",
    }:

        state["response"] = (
            "Thank you for using CrisisOps AI.\n\n"
            "Have a productive day!"
        )

        return state

    # -----------------------------
    # Default
    # -----------------------------

    state["response"] = (
        "Hello! How can I assist you with NovaRetail's supply chain today?"
    )

    return state