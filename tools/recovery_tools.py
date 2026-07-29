"""
Recovery Tools

Recovery planning for NovaRetail Phase 2.
Compatible with the new datasets.
"""

from tools.shipment_tools import track_shipment
from tools.inventory_tools import check_inventory
from tools.supplier_tools import find_alternative_suppliers


# -------------------------------------------------------
# Shipment Recovery
# -------------------------------------------------------

def recommend_recovery_action(shipment_id: str):

    shipment = track_shipment(shipment_id)

    if "error" in shipment:
        return shipment

    if shipment["delay_days"] > 0:

        priority = (
            "Critical"
            if shipment["risk_score"] >= 90
            else "High"
        )

        return {

            "shipment_id": shipment_id,

            "issue": "Shipment Delayed",

            "delay_days": shipment["delay_days"],

            "risk_score": shipment["risk_score"],

            "recommended_action": (
                "Contact carrier, evaluate alternate routes, "
                "notify stakeholders and monitor delivery."
            ),

            "priority": priority

        }

    return {

        "shipment_id": shipment_id,

        "recommended_action": "No recovery action required.",

        "priority": "Low"

    }


# -------------------------------------------------------
# Supplier Alternatives
# -------------------------------------------------------

def compare_supplier_alternatives(product_id: str):

    suppliers = find_alternative_suppliers(product_id)

    if isinstance(suppliers, dict):
        return suppliers

    comparison = []

    for supplier in suppliers:

        comparison.append({

            "supplier_id": supplier["supplier_id"],

            "supplier_name": supplier["supplier_name"],

            "rating": supplier["rating"],

            "location": supplier["location"],

            "country": supplier["country"],

            "primary_warehouse": supplier["primary_warehouse"],

            "available": supplier["available"]

        })

    return comparison


# -------------------------------------------------------
# Inventory Summary
# -------------------------------------------------------

def warehouse_stock_summary(product_id: str):

    inventory = check_inventory(product_id)

    if "error" in inventory:
        return inventory

    return {

        "product_id": inventory["product_id"],

        "product_name": inventory["product_name"],

        "warehouse_id": inventory["warehouse_id"],

        "quantity": inventory["quantity"],

        "minimum_required": inventory["minimum_required"],

        "status": inventory["status"]

    }


# -------------------------------------------------------
# Complete Recovery Plan
# -------------------------------------------------------

def generate_recovery_plan(
    shipment_id: str,
    product_id: str
):

    shipment = recommend_recovery_action(shipment_id)

    inventory = warehouse_stock_summary(product_id)

    suppliers = compare_supplier_alternatives(product_id)

    return {

        "shipment_recovery": shipment,

        "inventory_status": inventory,

        "alternative_suppliers": suppliers

    }


# -------------------------------------------------------
# Business Continuity Plan
# -------------------------------------------------------

def business_continuity_plan(
    shipment_id: str,
    product_id: str
):

    plan = generate_recovery_plan(
        shipment_id,
        product_id
    )

    plan["recommendations"] = [

        "Increase safety stock if inventory is low.",

        "Engage alternate suppliers if shipment delay exceeds SLA.",

        "Monitor transportation and weather risks.",

        "Notify operations and customer service teams.",

        "Review predictive risk dashboard before approving mitigation."

    ]

    return plan