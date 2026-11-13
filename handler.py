import json
import os
from classes import Cab, RideRequest

cabs_file = "cabs.json"
requests_file = "requests.json"


def load_items(filename, item_class):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename) as f:
            return [item_class.from_dict(entry) for entry in json.load(f)]
    except (ValueError, KeyError, TypeError) as err:
        print(f"Warning: could not read '{filename}' ({err}). Starting empty.")
        return []


def save_items(filename, items):
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in items], f, indent=2)


def load_cabs():
    if not os.path.exists(cabs_file):
        # First run: start with a few sample cabs
        return [
            Cab("Ramesh", 4, "Delhi", "Morning"),
            Cab("Suresh", 3, "Jaipur", "Night"),
            Cab("Mukesh", 4, "Delhi", "Evening"),
        ]
    return load_items(cabs_file, Cab)


def save_cabs(cabs):
    save_items(cabs_file, cabs)


def load_requests():
    return load_items(requests_file, RideRequest)


def save_requests(requests):
    save_items(requests_file, requests)
