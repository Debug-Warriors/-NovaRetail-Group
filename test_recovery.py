from tools.recovery_tools import generate_recovery_plan

result = generate_recovery_plan(
    shipment_id="SHP101",
    product_name="Wireless Headphones",
    product_id="P100",
)

print(result)