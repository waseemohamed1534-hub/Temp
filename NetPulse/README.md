# NetPulse

A small modular FastAPI API for registering devices and recording alerts when a device transitions from online to offline. Device and alert state is held in memory and resets when the process restarts.

## Run

From the project root, create and activate a virtual environment, install the requirements, and start the API:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open the interactive API documentation at http://127.0.0.1:8000/docs.

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/devices` | Register a device (returns `201`; duplicate IDs return `409`) |
| `GET` | `/devices` | List registered devices |
| `GET` | `/devices/{device_id}` | Get one device (unknown IDs return `404`) |
| `PATCH` | `/devices/{device_id}/status` | Update a device status (unknown IDs return `404`) |
| `GET` | `/alerts` | List recorded offline-transition alerts |
| `GET` | `/health` | Return `{"status":"ok"}` |

Device types are `router`, `switch`, and `server`; statuses are `online` and `offline`. Device IP addresses must be valid IPv4 addresses.

To verify the alert behavior in `/docs`, register a device with status `online`, PATCH its status to `offline` twice, then GET `/alerts`. Only the first online-to-offline transition creates an alert. Registering an initially offline device and repeating an offline update do not create alerts.

## Test

```bash
python -m pytest -q
```

The application is a modular monolith: routes handle HTTP and translate service errors to HTTP responses, the service owns business rules, the repository owns in-memory storage, and the event module records transition alerts. A later database-backed repository can replace the in-memory storage while keeping the route and service responsibilities unchanged. No real devices are contacted, and device and alert state resets when the process restarts.