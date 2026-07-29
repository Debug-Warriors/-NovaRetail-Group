"""
Shipment Tools

Shipment operations for NovaRetail.
Compatible with the Phase 2 shipments.json dataset.
"""

import json
from pathlib import Path

SHIPMENT_FILE = Path("data/shipments.json")


def load_shipments():
    if not SHIPMENT_FILE.exists():
        return []

    with open(SHIPMENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------------------------------------
# Track Shipment
# -----------------------------------------------------

def track_shipment(shipment_id: str):

    shipments = load_shipments()

    for shipment in shipments:

        if shipment["shipment_id"].lower() == shipment_id.lower():

            return {
                "shipment_id": shipment["shipment_id"],
                "order_id": shipment["order_id"],
                "product_id": shipment["product_id"],
                "supplier_id": shipment["supplier_id"],
                "warehouse_id": shipment["warehouse_id"],
                "carrier": shipment["carrier"],
                "origin": shipment["origin"],
                "destination": shipment["destination"],
                "route": shipment["route"],
                "status": shipment["status"],
                "current_location": shipment["current_location"],
                "expected_delivery": shipment["expected_delivery"],
                "delay_days": shipment["delay_days"],
                "weather_risk": shipment["weather_risk"],
                "traffic_status": shipment["traffic_status"],
                "carrier_performance": shipment["carrier_performance"],
                "risk_score": shipment["risk_score"],
            }

    return {
        "error": f"Shipment {shipment_id} not found."
    }


# -----------------------------------------------------
# Delay Check
# -----------------------------------------------------

def check_shipment_delay(shipment_id: str):

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment["shipment_id"],
        "status": shipment["status"],
        "delayed": shipment["delay_days"] > 0,
        "delay_days": shipment["delay_days"],
    }


# -----------------------------------------------------
# Current Location
# -----------------------------------------------------

def get_shipment_location(shipment_id: str):

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment["shipment_id"],
        "current_location": shipment["current_location"],
    }


# -----------------------------------------------------
# Affected Orders
# -----------------------------------------------------

def identify_affected_orders(shipment_id: str):

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    if shipment["delay_days"] == 0:

        return {
            "shipment_id": shipment_id,
            "affected_orders": [],
            "count": 0,
            "message": "No affected orders."
        }

    return {
        "shipment_id": shipment_id,
        "affected_orders": [
            shipment["order_id"]
        ],
        "count": 1,
        "message": "This order may be delayed."
    }


# -----------------------------------------------------
# Reroute Shipment
# -----------------------------------------------------

def reroute_shipment(shipment_id: str):

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment_id,
        "status": "Rerouted",
        "new_route": "Alternative Route Assigned",
        "message": "Shipment rerouted successfully."
    }