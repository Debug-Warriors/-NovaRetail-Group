"""
Supplier Tools

Supplier management operations for NovaRetail.
Compatible with the Phase 2 suppliers dataset.
"""

import json
from pathlib import Path

SUPPLIER_FILE = Path("data/suppliers.json")


# -------------------------------------------------------
# Load Suppliers
# -------------------------------------------------------

def load_suppliers():

    if not SUPPLIER_FILE.exists():
        return []

    with open(SUPPLIER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# -------------------------------------------------------
# Find Supplier
# -------------------------------------------------------

def find_supplier(supplier_name: str):

    suppliers = load_suppliers()

    for supplier in suppliers:

        if supplier["name"].lower() == supplier_name.lower():

            return supplier

    return {
        "error": f"Supplier '{supplier_name}' not found."
    }


# -------------------------------------------------------
# Supplier Availability
# -------------------------------------------------------

def check_supplier_availability(supplier_name: str):

    supplier = find_supplier(supplier_name)

    if "error" in supplier:
        return supplier

    return {

        "supplier_id": supplier["supplier_id"],

        "supplier_name": supplier["name"],

        "available": supplier["available"],

        "rating": supplier["rating"],

        "location": supplier["location"],

        "country": supplier["country"],

        "primary_warehouse": supplier["primary_warehouse"],

        "products": supplier["products"]

    }


# -------------------------------------------------------
# Alternative Suppliers
# -------------------------------------------------------

def find_alternative_suppliers(product_id: str):

    suppliers = load_suppliers()

    alternatives = []

    for supplier in suppliers:

        if (
            product_id in supplier["products"]
            and supplier["available"]
        ):

            alternatives.append({

                "supplier_id": supplier["supplier_id"],

                "supplier_name": supplier["name"],

                "rating": supplier["rating"],

                "location": supplier["location"],

                "country": supplier["country"],

                "primary_warehouse": supplier["primary_warehouse"],

                "available": supplier["available"]

            })

    alternatives.sort(
        key=lambda x: x["rating"],
        reverse=True
    )

    return alternatives


# -------------------------------------------------------
# Top Rated Suppliers
# -------------------------------------------------------

def get_top_suppliers(limit=5):

    suppliers = load_suppliers()

    suppliers.sort(
        key=lambda x: x["rating"],
        reverse=True
    )

    return suppliers[:limit]