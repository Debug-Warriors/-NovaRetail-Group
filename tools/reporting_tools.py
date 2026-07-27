"""
Reporting Tools

Simulates NovaRetail reporting system.
"""

from tools.incident_tools import list_open_incidents


def generate_incident_summary():

    """
    Generate summary of active incidents.
    """

    incidents = list_open_incidents()


    if not incidents:

        return {
            "message":
                "No open incidents."
        }


    return {

        "total_open_incidents":
            len(incidents),

        "incidents":
            incidents

    }



def generate_operational_report():

    """
    Generate high-level operations report.
    """

    incidents = list_open_incidents()


    high_priority = [

        incident
        for incident in incidents
        if incident["severity"].lower()
        == "high"

    ]


    return {

        "open_incidents":
            len(incidents),

        "high_priority_incidents":
            len(high_priority),

        "system_status":
            "Operational"

    }



def create_stakeholder_update():

    """
    Generate update information
    for business stakeholders.
    """

    report = generate_operational_report()


    return {

        "audience":
            "COO and Supply Chain Leadership",

        "summary":
            report,

        "message":
            "Supply chain operations are being monitored. "
            "Critical disruptions are escalated."

    }