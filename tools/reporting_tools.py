"""
Reporting Tools

Reporting operations for NovaRetail.
Compatible with the Phase 2 datasets.
"""

from datetime import datetime

from tools.incident_tools import (
    incident_summary,
    list_open_incidents,
    list_high_priority_incidents,
)


# -------------------------------------------------------
# Incident Summary
# -------------------------------------------------------

def generate_incident_summary():
    """
    Generate summary of current incidents.
    """

    summary = incident_summary()

    return {

        "report_date": datetime.now().strftime("%Y-%m-%d"),

        "total_incidents": summary["total_incidents"],

        "open_incidents": summary["open_incidents"],

        "resolved_incidents": summary["resolved_incidents"],

        "escalated_incidents": summary["escalated_incidents"],

        "high_priority_incidents": summary["high_priority_incidents"],

        "incidents": list_open_incidents()

    }


# -------------------------------------------------------
# Operational Report
# -------------------------------------------------------

def generate_operational_report():
    """
    Generate an operational overview.
    """

    summary = incident_summary()

    if summary["high_priority_incidents"] > 5:
        system_status = "High Risk"

    elif summary["open_incidents"] > 10:
        system_status = "Attention Required"

    else:
        system_status = "Operational"

    return {

        "report_date": datetime.now().strftime("%Y-%m-%d"),

        "system_status": system_status,

        "total_incidents": summary["total_incidents"],

        "open_incidents": summary["open_incidents"],

        "resolved_incidents": summary["resolved_incidents"],

        "escalated_incidents": summary["escalated_incidents"],

        "high_priority_incidents": summary["high_priority_incidents"]

    }


# -------------------------------------------------------
# Stakeholder Update
# -------------------------------------------------------

def create_stakeholder_update():
    """
    Generate executive update.
    """

    report = generate_operational_report()

    return {

        "audience": "COO and Supply Chain Leadership",

        "generated_on": datetime.now().strftime("%Y-%m-%d"),

        "summary": report,

        "message": (
            "Operations are continuously monitored. "
            "High-priority incidents are escalated immediately. "
            "Predictive Risk Intelligence proactively identifies "
            "potential disruptions before they impact operations."
        )

    }


# -------------------------------------------------------
# Executive Dashboard
# -------------------------------------------------------

def generate_dashboard():
    """
    Dashboard summary for the UI.
    """

    summary = incident_summary()

    return {

        "system_status": (
            "Operational"
            if summary["open_incidents"] < 10
            else "Attention Required"
        ),

        "total_incidents": summary["total_incidents"],

        "open_incidents": summary["open_incidents"],

        "resolved_incidents": summary["resolved_incidents"],

        "high_priority_incidents": summary["high_priority_incidents"]

    }


# -------------------------------------------------------
# Reporting Metrics
# -------------------------------------------------------

def reporting_metrics():
    """
    KPI metrics for reporting.
    """

    summary = incident_summary()

    total = summary["total_incidents"]

    if total == 0:

        resolution_rate = 100

    else:

        resolution_rate = round(
            (summary["resolved_incidents"] / total) * 100,
            1
        )

    return {

        "total_incidents": total,

        "resolution_rate": resolution_rate,

        "open_incidents": summary["open_incidents"],

        "high_priority_incidents": summary["high_priority_incidents"]

    }