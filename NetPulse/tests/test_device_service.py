import pytest

from app.models import DeviceCreate
from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


@pytest.fixture
def service() -> DeviceService:
    return DeviceService(InMemoryDeviceRepository())


def make_device(status: str = "online") -> DeviceCreate:
    return DeviceCreate(
        device_id="RTR-101",
        name="Branch Router",
        device_type="router",
        ip_address="192.168.10.1",
        status=status,
    )


def test_register_device(service: DeviceService) -> None:
    device = service.register(make_device())

    assert device.device_id == "RTR-101"
    assert device.status == "online"
    assert len(service.list()) == 1


def test_duplicate_device_id_raises_error(service: DeviceService) -> None:
    service.register(make_device())

    with pytest.raises(DeviceAlreadyExistsError):
        service.register(make_device())


def test_missing_device_raises_error(service: DeviceService) -> None:
    with pytest.raises(DeviceNotFoundError):
        service.get("MISSING")

    with pytest.raises(DeviceNotFoundError):
        service.update_status("MISSING", "offline")


def test_initial_offline_registration_creates_no_alert(service: DeviceService) -> None:
    service.register(make_device(status="offline"))

    assert service.list_alerts() == []


def test_online_to_offline_creates_one_alert(service: DeviceService) -> None:
    service.register(make_device())

    service.update_status("RTR-101", "offline")
    alerts = service.list_alerts()

    assert len(alerts) == 1
    assert alerts[0].device_id == "RTR-101"
    assert "online to offline" in alerts[0].message
    assert alerts[0].timestamp.utcoffset().total_seconds() == 0


def test_repeated_offline_update_does_not_create_another_alert(
    service: DeviceService,
) -> None:
    service.register(make_device())

    service.update_status("RTR-101", "offline")
    service.update_status("RTR-101", "offline")

    assert len(service.list_alerts()) == 1