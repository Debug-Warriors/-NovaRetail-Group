"""
Supplier Tools

Simulates NovaRetail Supplier Management System.
"""

import json
from pathlib import Path

SUPPLIER_FILE = Path("data/suppliers.json")


def load_suppliers():
    """Load supplier data."""

    if not SUPPLIER_FILE.exists():
        return []

    with open(SUPPLIER_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_supplier(supplier_name: str):
    """
    Find supplier by name.
    """

    suppliers = load_suppliers()

    for supplier in suppliers:

        if supplier["name"].lower() == supplier_name.lower():
            return supplier

    return {
        "error": f"Supplier '{supplier_name}' not found."
    }


def check_supplier_availability(supplier_name: str):
    """
    Check supplier availability.
    """

    supplier = find_supplier(supplier_name)

    if "error" in supplier:
        return supplier

    return {
        "supplier": supplier["name"],
        "available": supplier["available"],
        "rating": supplier["rating"],
        "location": supplier["location"]
    }


def find_alternative_suppliers(product: str):
    """
    Find available suppliers for a product.
    """

    suppliers = load_suppliers()

    alternatives = []

    for supplier in suppliers:

        if (
            product.lower() in [p.lower() for p in supplier["products"]]
            and supplier["available"]
        ):

            alternatives.append(
                {
                    "supplier": supplier["name"],
                    "rating": supplier["rating"],
                    "location": supplier["location"],
                    "available": supplier["available"],
                }
            )

    if not alternatives:

        return {
            "message": "No available alternative suppliers found."
        }

    alternatives.sort(
        key=lambda x: x["rating"],
        reverse=True
    )

    return alternatives