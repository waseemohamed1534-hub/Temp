from datetime import datetime, timezone

from app.models import AlertResponse
from app.repositories.device_repository import InMemoryDeviceRepository


def create_offline_alert(
    repository: InMemoryDeviceRepository,
    device_id: str,
) -> AlertResponse:
    alert = AlertResponse(
        device_id=device_id,
        message=f"Device {device_id} changed from online to offline.",
        timestamp=datetime.now(timezone.utc),
    )
    return repository.save_alert(alert)