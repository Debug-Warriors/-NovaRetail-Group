"""
Incident Tools

Simulates NovaRetail Incident Management System.
"""

import json
from pathlib import Path
from datetime import datetime
import uuid

INCIDENT_FILE = Path("data/incidents.json")


def load_incidents():
    """Load all incidents."""

    if not INCIDENT_FILE.exists():
        return []

    with open(INCIDENT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_incidents(incidents):

    with open(INCIDENT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            incidents,
            file,
            indent=4
        )


def create_incident(
    title: str,
    description: str,
    severity: str
):
    """
    Create a new incident.
    """

    incidents = load_incidents()

    incident = {

        "incident_id":
            str(uuid.uuid4())[:8].upper(),

        "title":
            title,

        "description":
            description,

        "severity":
            severity,

        "status":
            "Open",

        "created_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    }

    incidents.append(incident)

    save_incidents(incidents)

    return incident


def get_incident(incident_id):

    incidents = load_incidents()

    for incident in incidents:

        if (
            incident["incident_id"].lower()
            ==
            incident_id.lower()
        ):
            return incident

    return {
        "error": "Incident not found"
    }


def escalate_incident(incident_id):

    incidents = load_incidents()

    for incident in incidents:

        if (
            incident["incident_id"].lower()
            ==
            incident_id.lower()
        ):

            incident["status"] = "Escalated"

            save_incidents(incidents)

            return incident

    return {
        "error": "Incident not found"
    }


def list_open_incidents():

    incidents = load_incidents()

    return [
        incident
        for incident in incidents
        if incident["status"] == "Open"
    ]