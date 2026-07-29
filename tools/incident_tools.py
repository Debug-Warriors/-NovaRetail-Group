"""
Incident Tools

Incident Management operations for NovaRetail.
Compatible with the Phase 2 incidents dataset.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime

INCIDENT_FILE = Path("data/incidents.json")


# -------------------------------------------------------
# Load Incidents
# -------------------------------------------------------

def load_incidents():

    if not INCIDENT_FILE.exists():
        return []

    with open(INCIDENT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------------
# Save Incidents
# -------------------------------------------------------

def save_incidents(incidents):

    with open(INCIDENT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            incidents,
            file,
            indent=4
        )


# -------------------------------------------------------
# Create Incident
# -------------------------------------------------------

def create_incident(
    shipment_id="",
    order_id="",
    supplier_id="",
    warehouse_id="",
    product_id="",
    category="General",
    severity="Medium",
    root_cause="Under Investigation",
    impact="Unknown",
    assigned_team="Operations",
    risk_score=50
):
    """
    Create a new incident.
    """

    incidents = load_incidents()

    incident = {

        "incident_id": str(uuid.uuid4())[:8].upper(),

        "shipment_id": shipment_id,

        "order_id": order_id,

        "supplier_id": supplier_id,

        "warehouse_id": warehouse_id,

        "product_id": product_id,

        "category": category,

        "severity": severity,

        "status": "Open",

        "reported_date": datetime.now().strftime("%Y-%m-%d"),

        "root_cause": root_cause,

        "impact": impact,

        "assigned_team": assigned_team,

        "risk_score": risk_score

    }

    incidents.append(incident)

    save_incidents(incidents)

    return incident


# -------------------------------------------------------
# Get Incident
# -------------------------------------------------------

def get_incident(incident_id):

    incidents = load_incidents()

    for incident in incidents:

        if incident["incident_id"].lower() == incident_id.lower():

            return incident

    return {
        "error": f"Incident {incident_id} not found."
    }


# -------------------------------------------------------
# Escalate Incident
# -------------------------------------------------------

def escalate_incident(incident_id):

    incidents = load_incidents()

    for incident in incidents:

        if incident["incident_id"].lower() == incident_id.lower():

            incident["status"] = "Escalated"

            if incident["risk_score"] < 90:
                incident["risk_score"] += 20

            save_incidents(incidents)

            return incident

    return {
        "error": f"Incident {incident_id} not found."
    }


# -------------------------------------------------------
# Resolve Incident
# -------------------------------------------------------

def resolve_incident(incident_id):

    incidents = load_incidents()

    for incident in incidents:

        if incident["incident_id"].lower() == incident_id.lower():

            incident["status"] = "Resolved"

            save_incidents(incidents)

            return incident

    return {
        "error": f"Incident {incident_id} not found."
    }


# -------------------------------------------------------
# List Open Incidents
# -------------------------------------------------------

def list_open_incidents():

    incidents = load_incidents()

    return [

        incident

        for incident in incidents

        if incident["status"].lower() == "open"

    ]


# -------------------------------------------------------
# List High Priority Incidents
# -------------------------------------------------------

def list_high_priority_incidents():

    incidents = load_incidents()

    return [

        incident

        for incident in incidents

        if incident["severity"].lower() in ["high", "critical"]

    ]


# -------------------------------------------------------
# Incident Summary
# -------------------------------------------------------

def incident_summary():

    incidents = load_incidents()

    open_incidents = [
        i for i in incidents
        if i["status"].lower() == "open"
    ]

    resolved_incidents = [
        i for i in incidents
        if i["status"].lower() == "resolved"
    ]

    escalated_incidents = [
        i for i in incidents
        if i["status"].lower() == "escalated"
    ]

    high_priority = [
        i for i in incidents
        if i["severity"].lower() in ["high", "critical"]
    ]

    return {

        "total_incidents": len(incidents),

        "open_incidents": len(open_incidents),

        "resolved_incidents": len(resolved_incidents),

        "escalated_incidents": len(escalated_incidents),

        "high_priority_incidents": len(high_priority)

    }