import json
from data import Cab, RideRequest

CABS_FILE = "cabs.json"
REQUESTS_FILE = "pending_requests.json"


def load(filename, cls):
    try:
        with open(filename) as f:
            return [cls.from_dict(item) for item in json.load(f)]
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Warning: could not read '{filename}' ({e}). Starting empty.")
        return []


def save(filename, items):
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=2)


def load_cabs():
    return load(CABS_FILE, Cab)


def load_requests():
    return load(REQUESTS_FILE, RideRequest)


def save_cabs(cabs):
    save(CABS_FILE, cabs)


def save_requests(requests):
    save(REQUESTS_FILE, requests)
