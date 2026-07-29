"""
Inventory Tools

Inventory operations for NovaRetail.
Compatible with the Phase 2 inventory dataset.
"""

import json
from pathlib import Path

INVENTORY_FILE = Path("data/inventory.json")


def load_inventory():

    if not INVENTORY_FILE.exists():
        return []

    with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------------
# Check Product Inventory
# -------------------------------------------------------

def check_inventory(product_id: str):

    inventory = load_inventory()

    for item in inventory:

        if item["product_id"].lower() == product_id.lower():

            return {

                "product_id": item["product_id"],

                "product_name": item["product_name"],

                "supplier_id": item["supplier_id"],

                "warehouse_id": item["warehouse_id"],

                "quantity": item["quantity"],

                "minimum_required": item["minimum_required"],

                "maximum_capacity": item["maximum_capacity"],

                "unit_cost": item["unit_cost"],

                "status": item["status"]

            }

    return {
        "error": f"Product {product_id} not found."
    }


# -------------------------------------------------------
# Inventory Shortage
# -------------------------------------------------------

def check_inventory_shortage(product_id: str):

    result = check_inventory(product_id)

    if "error" in result:
        return result

    shortage = result["quantity"] < result["minimum_required"]

    return {

        "product_id": result["product_id"],

        "product_name": result["product_name"],

        "shortage": shortage,

        "available_quantity": result["quantity"],

        "minimum_required": result["minimum_required"],

        "status": result["status"]

    }


# -------------------------------------------------------
# Warehouse Availability
# -------------------------------------------------------

def warehouse_availability(warehouse_id: str):

    inventory = load_inventory()

    products = []

    for item in inventory:

        if item["warehouse_id"].lower() == warehouse_id.lower():

            products.append(item)

    if not products:

        return {
            "error": f"Warehouse {warehouse_id} not found."
        }

    return {

        "warehouse_id": warehouse_id,

        "product_count": len(products),

        "products": products,

        "status": "Operational"

    }


# -------------------------------------------------------
# Identify All Shortages
# -------------------------------------------------------

def identify_inventory_shortage():

    inventory = load_inventory()

    shortages = []

    for item in inventory:

        if item["quantity"] < item["minimum_required"]:

            shortages.append({

                "product_id": item["product_id"],

                "product_name": item["product_name"],

                "warehouse_id": item["warehouse_id"],

                "quantity": item["quantity"],

                "minimum_required": item["minimum_required"],

                "status": item["status"]

            })

    return {

        "count": len(shortages),

        "shortages": shortages

    }