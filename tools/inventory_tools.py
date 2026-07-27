"""
Inventory Tools

Simulates NovaRetail Inventory Management System APIs.

Functions:
- Check product inventory
- Detect shortages
- Check warehouse stock
"""

import json
from pathlib import Path


INVENTORY_FILE = Path("data/inventory.json")



def load_inventory():

    """
    Load inventory data.
    """

    if not INVENTORY_FILE.exists():
        return []

    with open(
        INVENTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def check_inventory(product_id: str):

    """
    Find inventory details for a product.

    Example:
        check_inventory("P100")
    """

    inventory = load_inventory()


    for item in inventory:

        if item["product_id"].lower() == product_id.lower():

            return {

                "product_id":
                    item["product_id"],

                "product_name":
                    item["product_name"],

                "warehouse":
                    item["warehouse"],

                "quantity":
                    item["quantity"],

                "minimum_required":
                    item["minimum_required"],

                "status":
                    "Available"
                    if item["quantity"] >= item["minimum_required"]
                    else "Low Stock"

            }


    return {
        "error":
            f"Product {product_id} not found"
    }



def check_inventory_shortage(product_id: str):

    """
    Check whether a product has shortage.
    """

    result = check_inventory(product_id)


    if "error" in result:
        return result


    shortage = (
        result["quantity"]
        <
        result["minimum_required"]
    )


    return {

        "product_id":
            product_id,

        "shortage":
            shortage,

        "available_quantity":
            result["quantity"],

        "required_quantity":
            result["minimum_required"]

    }



def warehouse_availability(warehouse_name: str):

    """
    Check warehouse capacity/status.
    """

    inventory = load_inventory()


    products = []


    for item in inventory:

        if (
            item["warehouse"].lower()
            ==
            warehouse_name.lower()
        ):

            products.append(item)



    if not products:

        return {
            "error":
            "Warehouse not found"
        }



    return {

        "warehouse":
            warehouse_name,

        "products":
            products,

        "status":
            "Operational"

    }
def identify_inventory_shortage():
    """
    Return all products that are below their minimum required quantity.
    """

    inventory = load_inventory()

    shortages = []

    for item in inventory:

        if item["quantity"] < item["minimum_required"]:

            shortages.append({

                "product_id": item["product_id"],

                "product_name": item["product_name"],

                "warehouse": item["warehouse"],

                "quantity": item["quantity"],

                "minimum_required": item["minimum_required"]

            })

    return {

        "count": len(shortages),

        "shortages": shortages

    }