from classes import RideRequest, cities, time_slots
from handler import load_cabs, save_cabs, load_requests, save_requests


def add_ride_request(requests):
    print("\n--- New Ride Request ---")
    name = input("Student's name: ")
    destination = input(f"Destination ({'/'.join(cities)}): ")
    time_slot = input(f"Time slot ({'/'.join(time_slots)}): ")
    year = input("Year (1 to 5): ").strip()

    if not year.isdigit():
        print("Error: year must be a number from 1 to 5.")
        return

    try:
        request = RideRequest(name, destination, time_slot, int(year))
    except ValueError as err:
        print(f"Error: {err}")
        return

    requests.append(request)
    print(f"Added request: {request}")


def print_list(items, empty_message):
    if not items:
        print(empty_message)
    for number, item in enumerate(items, 1):
        print(f"{number}. {item}")


def view_status(requests, cabs):
    print("\n=== Students Currently Waiting ===")
    print_list(requests, "No students waiting.")

    print("\n=== Open Cabs ===")
    print_list([c for c in cabs if not c.has_left], "None")

    print("\n=== Already Left ===")
    print_list([c for c in cabs if c.has_left], "None")


def main():
    cabs = load_cabs()
    requests = load_requests()

    while True:
        print("\n==============================")
        print("      Cab Sharing Menu")
        print("==============================")
        print("1. Add a new ride request.")
        print("2. See everyone still waiting, plus all cabs.")
        print("3. Quit the app.")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_ride_request(requests)
        elif choice == "2":
            view_status(requests, cabs)
        elif choice == "3":
            save_cabs(cabs)
            save_requests(requests)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
