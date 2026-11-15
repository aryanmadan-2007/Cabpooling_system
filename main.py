from data import RideRequest, cities, time_slots
from file_handle import load_cabs, save_cabs, load_requests, save_requests


def print_numbered(items):
    if not items:
        print("None")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")


def add_ride_request(pending_requests, cabs):
    print("\n--- New Ride Request ---")
    name = input("Student's name: ")
    destination = input(f"Destination ({'/'.join(cities)}): ")
    time_slot = input(f"Time slot ({'/'.join(time_slots)}): ")
    try:
        year = int(input("Year (1 to 5): "))
        request = RideRequest(name, destination, time_slot, year)
    except ValueError as err:
        print(f"Error: {err}")
        return
    pending_requests.append(request)
    print(f"Added request: {request}")


def view_status(pending_requests, cabs):
    print("\n=== Students Currently Waiting ===")
    print_numbered(pending_requests)
    print("\n=== Open Cabs ===")
    print_numbered([c for c in cabs if not c.has_left])
    print("\n=== Already Left ===")
    print_numbered([c for c in cabs if c.has_left])


def find_matches(pending_requests, cabs):
    print("\n=== Match Preview (No Seats Assigned) ===")
    open_cabs = [c for c in cabs if not c.has_left]
    if not open_cabs:
        print("No open cabs available.")
        return

    pool = list(pending_requests)  # copy
    for i, cab in enumerate(open_cabs, 1):
        print(f"\n{i}. Cab: {cab.driver_name} -> {cab.destination} [{cab.time_slot}] "
              f"(Available seats: {cab.free_seats()}/{cab.seats})")
        matched = cab.matches(pool)
        if not matched:
            print("Matched students: None")
        for student in matched:
            print(f"- {student.student_name} (Year {student.year}) | Submitted: {student.submitted_at}")
            pool.remove(student)


def dispatch_cab(pending_requests, cabs):
    print("\n=== Let a Cab Leave ===")
    open_cabs = [c for c in cabs if not c.has_left]
    if not open_cabs:
        print("No open cabs available to send off.")
        return
    print_numbered(open_cabs)

    choice = input("Choose an open cab to dispatch (0 to cancel): ").strip()
    if not choice.isdigit() or not 0 <= int(choice) <= len(open_cabs):
        print("Invalid choice.")
        return
    if choice == "0":
        print("Dispatch cancelled.")
        return

    cab = open_cabs[int(choice) - 1]
    boarded = cab.dispatch(pending_requests)
    print(f"\nDispatched: {cab.driver_name} -> {cab.destination} [{cab.time_slot}] "
          f"| Final Seats: {len(cab.students)}/{cab.seats}")
    if boarded:
        print("Newly boarded students (removed from waiting list):")
        for student in boarded:
            print(f"  - {student.student_name} (Year {student.year})")
    else:
        print("No new waiting students boarded.")


MENU = {
    "1": ("Add a new ride request.", add_ride_request),
    "2": ("See everyone still waiting, plus all cabs.", view_status),
    "3": ("Find matches (preview).", find_matches),
    "4": ("Let a cab leave.", dispatch_cab),
}


def main():
    cabs = load_cabs()
    pending_requests = load_requests()

    while True:
        print("\n===== Cab Sharing Menu =====")
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        print("5. Quit the app.")

        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            save_cabs(cabs)
            save_requests(pending_requests)
            print("Data saved. Goodbye!")
            break
        if choice in MENU:
            MENU[choice][1](pending_requests, cabs)
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
