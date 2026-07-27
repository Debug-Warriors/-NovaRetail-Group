"""
Supply Chain Shared State

This object is passed between all LangGraph agents.
"""

from typing import TypedDict, Any, List


class SupplyChainState(TypedDict):

    # -----------------------------
    # Conversation
    # -----------------------------

    messages: List[Any]


    # -----------------------------
    # User Input
    # -----------------------------

    user_query: str


    # -----------------------------
    # Supervisor Routing
    # -----------------------------

    intent: str


    # -----------------------------
    # Current Executing Agent
    # -----------------------------

    current_agent: str


    # -----------------------------
    # Tool Output
    # -----------------------------

    tool_result: dict


    # -----------------------------
    # Final Assistant Response
    # -----------------------------

    response: str


    # -----------------------------
    # Human Approval
    # Used for:
    # - Create Incident
    # - Select Supplier
    # - Reroute Shipment
    # - Recovery Approval
    # -----------------------------

    approval: bool


    # -----------------------------
    # Memory
    # Stores conversation context
    # -----------------------------

    memory: dict

    blocked:bool