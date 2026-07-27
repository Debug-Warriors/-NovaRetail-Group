"""
Shipment Tools

These functions simulate NovaRetail's
Shipment Tracking Platform API.

Later these can be replaced with REST API calls.
"""

import json
from pathlib import Path


SHIPMENT_FILE = Path("data/shipments.json")


def load_shipments():
    """
    Load shipment data from mock database.
    """

    if not SHIPMENT_FILE.exists():
        return []

    with open(
        SHIPMENT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def track_shipment(shipment_id: str):
    """
    Find shipment details.
    """

    shipments = load_shipments()

    for shipment in shipments:

        if shipment["shipment_id"].lower() == shipment_id.lower():

            return {
                "shipment_id": shipment["shipment_id"],
                "status": shipment["status"],
                "location": shipment["location"],
                "warehouse": shipment["warehouse"],
                "expected_delivery": shipment["expected_delivery"],
                "delay": shipment.get("delay", "No delay"),
            }

    return {
        "error": f"Shipment {shipment_id} not found."
    }


def check_shipment_delay(shipment_id: str):
    """
    Check shipment delay.
    """

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment["shipment_id"],
        "status": shipment["status"],
        "delayed": shipment["status"].lower() == "delayed",
        "delay": shipment["delay"],
    }


def get_shipment_location(shipment_id: str):
    """
    Get shipment location.
    """

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment["shipment_id"],
        "current_location": shipment["location"],
    }


def identify_affected_orders(shipment_id: str):
    """
    Mock affected orders.

    Later this can use orders.json.
    """

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    if shipment["status"].lower() != "delayed":

        return {
            "shipment_id": shipment_id,
            "affected_orders": [],
            "count": 0,
            "message": "No affected orders."
        }

    return {
        "shipment_id": shipment_id,
        "affected_orders": [
            "ORD1001",
            "ORD1002",
            "ORD1003",
        ],
        "count": 3,
        "message": "Orders may experience delivery delays."
    }


def reroute_shipment(shipment_id: str):
    """
    Mock rerouting operation.
    """

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    return {
        "shipment_id": shipment_id,
        "status": "Rerouted",
        "message": "Shipment rerouted successfully."
    }