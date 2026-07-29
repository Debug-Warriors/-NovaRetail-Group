"""
Risk Intelligence Tools

Predictive analysis for NovaRetail Phase 2.

These functions analyze operational data from
multiple systems and identify potential risks
before disruptions occur.
"""

from tools.shipment_tools import load_shipments
from tools.inventory_tools import load_inventory
from tools.supplier_tools import load_suppliers

import json
from pathlib import Path


WEATHER_FILE = Path("data/weather_events.json")
DEMAND_FILE = Path("data/demand_forecast.json")
WAREHOUSE_FILE = Path("data/warehouses.json")
ROUTES_FILE = Path("data/transport_routes.json")
PERFORMANCE_FILE = Path("data/supplier_performance_history.json")
EVENTS_FILE = Path("data/external_events.json")


# -------------------------------------------------------
# Generic Loader
# -------------------------------------------------------

def load_json(path: Path):

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------------------------------
# Supplier Risk
# -------------------------------------------------------

def detect_supplier_risk():

    history = load_json(PERFORMANCE_FILE)

    risks = []

    latest = {}

    for record in history:
        supplier = record["supplier_name"]
        latest[supplier] = record

    for supplier, rec in latest.items():

        score = 0
        reasons = []

        if rec["on_time_delivery_percent"] < 90:
            score += 40
            reasons.append(
                "On-time delivery below 90%"
            )

        if rec["average_delay_days"] > 1:
            score += 30
            reasons.append(
                "Average delays increasing"
            )

        if rec["trend"].lower() == "declining":
            score += 30
            reasons.append(
                "Supplier performance declining"
            )

        if score >= 50:

            risks.append({

                "type": "Supplier",

                "supplier": supplier,

                "risk_score": score,

                "confidence": min(score, 95),

                "reasons": reasons,

                "recommendation":
                    "Evaluate alternative suppliers."

            })

    return risks


# -------------------------------------------------------
# Inventory Risk
# -------------------------------------------------------

def detect_inventory_risk():

    inventory = load_inventory()

    demand = load_json(DEMAND_FILE)

    risks = []

    forecast = {
        d["product_id"]: d
        for d in demand
    }

    for item in inventory:

        product = item["product_id"]

        if product not in forecast:
            continue

        predicted = forecast[product]

        quantity = item["quantity"]

        expected = predicted["forecast_next_month"]

        if expected > quantity:

            score = 80

            risks.append({

                "type": "Inventory",

                "product_id": product,

                "product_name": item["product_name"],

                "risk_score": score,

                "confidence": 90,

                "reasons": [

                    "Forecast demand exceeds inventory",

                    f"Inventory={quantity}",

                    f"Forecast={expected}"

                ],

                "recommendation":

                    "Increase replenishment."

            })

    return risks

# -------------------------------------------------------
# Weather Risk
# -------------------------------------------------------

def detect_weather_risk():

    events = load_json(WEATHER_FILE)

    risks = []

    for event in events:

        severity = event["severity"].lower()

        if severity in ["high", "critical"]:

            risks.append({

                "type": "Weather",

                "location": event["region"],

                "risk_score": event["risk_score"],

                "confidence": int(event["confidence"] * 100),

                "reasons": [

                    f"Weather Event: {event['event_type']}",

                    f"Severity: {event['severity']}",

                    f"Route: {event['route']}",

                    f"Affected Shipments: {len(event['affected_shipments'])}"

                ],

                "recommendation":
                    "Review affected shipments and consider rerouting."

            })

    return risks
# -------------------------------------------------------
# Warehouse Capacity
# -------------------------------------------------------

def detect_capacity_risk():

    warehouses = load_json(WAREHOUSE_FILE)

    risks = []

    for warehouse in warehouses:

        util = warehouse["utilization_percentage"]

        if util >= 90:

            risks.append({

                "type": "Warehouse",

                "warehouse": warehouse["warehouse_name"],

                "risk_score": util,

                "confidence": 88,

                "reasons": [

                    f"Warehouse utilization is {util}%",

                    f"Available space: {warehouse['available_space']} units"

                ],

                "recommendation":
                    "Redirect future shipments or increase warehouse capacity."

            })

    return risks
# -------------------------------------------------------
# Transportation Risk
# -------------------------------------------------------

def detect_transport_risk():

    routes = load_json(ROUTES_FILE)

    risks = []

    for route in routes:

        if route["risk_score"] >= 80:

            risks.append({

                "type": "Transport",

                "route": route["route_name"],

                "risk_score": route["risk_score"],

                "confidence": 92,

                "reasons": [

                    f"Congestion: {route['congestion_level']}",

                    f"Weather Risk: {route['weather_risk']}",

                    f"Average Delay: {route['average_delay_hours']} hours"

                ],

                "recommendation":
                    "Consider rerouting shipments through an alternate route."

            })

    return risks
# -------------------------------------------------------
# External Events
# -------------------------------------------------------

def detect_external_risk():

    events = load_json(EVENTS_FILE)

    risks = []

    for event in events:

        if event["risk_score"] >= 80:

            risks.append({

                "type": "External",

                "event": event["event_name"],

                "risk_score": event["risk_score"],

                "confidence": 90,

                "reasons": [

                    event["expected_impact"]

                ],

                "recommendation":

                    "Prepare contingency plan."

            })

    return risks


# -------------------------------------------------------
# Overall Analysis
# -------------------------------------------------------

def calculate_overall_risk():

    all_risks = []

    all_risks.extend(detect_supplier_risk())
    all_risks.extend(detect_inventory_risk())
    all_risks.extend(detect_weather_risk())
    all_risks.extend(detect_capacity_risk())
    all_risks.extend(detect_transport_risk())
    all_risks.extend(detect_external_risk())

    if not all_risks:

        return {

            "overall_risk": "Low",

            "risk_score": 10,

            "confidence": 95,

            "risks": []

        }

    highest = max(
        r["risk_score"]
        for r in all_risks
    )

    if highest >= 90:
        level = "Critical"
    elif highest >= 75:
        level = "High"
    elif highest >= 50:
        level = "Medium"
    else:
        level = "Low"

    confidence = int(
        sum(
            r["confidence"]
            for r in all_risks
        ) / len(all_risks)
    )

    return {

        "overall_risk": level,

        "risk_score": highest,

        "confidence": confidence,

        "total_risks": len(all_risks),

        "risks": sorted(
            all_risks,
            key=lambda x: x["risk_score"],
            reverse=True
        )

    }