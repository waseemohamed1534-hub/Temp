from fastapi import FastAPI

from app.repositories.device_repository import InMemoryDeviceRepository
from app.routes.devices import create_devices_router
from app.services.device_service import DeviceService


repository = InMemoryDeviceRepository()
device_service = DeviceService(repository)

app = FastAPI(title="NetPulse Device Monitoring API")
app.include_router(create_devices_router(device_service))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}