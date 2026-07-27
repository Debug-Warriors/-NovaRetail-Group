"""
Recovery Tools

Provides recovery recommendations for
supply chain disruptions.
"""

from tools.shipment_tools import track_shipment
from tools.inventory_tools import check_inventory
from tools.supplier_tools import find_alternative_suppliers


def recommend_recovery_action(shipment_id: str):
    """
    Recommend recovery actions for a delayed shipment.
    """

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    status = shipment["status"]

    if status.lower() == "delayed":

        return {
            "shipment_id": shipment_id,
            "issue": "Shipment Delayed",
            "recommended_action": (
                "Contact carrier, notify stakeholders, "
                "and evaluate alternative suppliers."
            ),
            "priority": "High",
        }

    return {
        "shipment_id": shipment_id,
        "recommended_action": "No action required.",
        "priority": "Low",
    }


def compare_supplier_alternatives(product_name: str):
    """
    Compare available suppliers.
    """

    suppliers = find_alternative_suppliers(product_name)

    if isinstance(suppliers, dict):
        return suppliers

    comparison = []

    for supplier in suppliers:

        comparison.append(
            {
                "supplier": supplier["supplier"],
                "rating": supplier["rating"],
                "available": supplier["available"],
                "location": supplier["location"],
            }
        )

    return comparison


def warehouse_stock_summary(product_id: str):
    """
    Check stock for recovery planning.
    """

    inventory = check_inventory(product_id)

    if "error" in inventory:
        return inventory

    return {
        "product_id": inventory["product_id"],
        "warehouse": inventory["warehouse"],
        "available_quantity": inventory["quantity"],
        "status": inventory["status"],
    }


def generate_recovery_plan(
    shipment_id: str,
    product_name: str,
    product_id: str,
):
    """
    Combine shipment, inventory,
    and supplier information into one plan.
    """

    shipment = recommend_recovery_action(shipment_id)

    inventory = warehouse_stock_summary(product_id)

    suppliers = compare_supplier_alternatives(product_name)

    return {
        "shipment": shipment,
        "inventory": inventory,
        "alternative_suppliers": suppliers,
    }