from tools.incident_tools import create_incident

incident = create_incident(
    title="Shipment Delay",
    description="Shipment SHP101 delayed by 2 days",
    severity="High"
)

print(incident)