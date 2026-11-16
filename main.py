from file_handle import RideRequest, cities, time_slots
from data import load_cabs, load_requests, save_all

MENU = """
==============================
      Cab Sharing Menu
==============================
1. Add a new ride request.
2. See everyone still waiting, plus all cabs (both open and already left).
3. Find matches (preview).
4. Let a cab leave.
5. Quit the app."""


def show_list(items):
    if not items:
        print("None")
    for n, item in enumerate(items, start=1):
        print(f"{n}. {item}")


def open_cabs_of(cabs):
    return [cab for cab in cabs if not cab.has_left]


def add_ride_request(pending, cabs):
    print("\n--- New Ride Request ---")
    name = input("Student's name: ")
    destination = input(f"Destination ({'/'.join(cities)}): ")
    time_slot = input(f"Time slot ({'/'.join(time_slots)}): ")
    try:
        year = int(input("Year (1 to 5): "))
    except ValueError:
        print("Error: year must be a number from 1 to 5.")
        return
    try:
        request = RideRequest(name, destination, time_slot, year)
    except ValueError as err:
        print(f"Error: {err}")
        return
    pending.append(request)
    save_all(cabs, pending)
    print(f"Added request: {request}")


def view_status(pending, cabs):
    print("\n=== Students Currently Waiting ===")
    show_list(pending)
    print("\n=== Open Cabs ===")
    show_list(open_cabs_of(cabs))
    print("\n=== Already Left ===")
    show_list([cab for cab in cabs if cab.has_left])


def find_matches(pending, cabs):
    print("\n=== Match Preview (No Seats Assigned) ===")
    open_cabs = open_cabs_of(cabs)
    if not open_cabs:
        print("No open cabs available.")
        return

    taken = []  # so two cabs on the same route don't preview the same student
    for n, cab in enumerate(open_cabs, start=1):
        print(f"\n{n}. Cab: {cab.driver_name} -> {cab.destination} [{cab.time_slot}] "
              f"(Available seats: {cab.free_seats()}/{cab.seats})")
        matches = [r for r in cab.matching(pending) if r not in taken][:cab.free_seats()]
        taken.extend(matches)
        if not matches:
            print("Matched students: None")
        for r in matches:
            print(f"- {r.student_name} (Year {r.year}) | Submitted: {r.submitted_at}")


def dispatch_cab(pending, cabs):
    print("\n=== Let a Cab Leave ===")
    open_cabs = open_cabs_of(cabs)
    if not open_cabs:
        print("No open cabs available to send off.")
        return

    show_list(open_cabs)
    choice = input("Choose an open cab to dispatch (0 to cancel): ").strip()
    if choice == "0":
        print("Dispatch cancelled.")
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(open_cabs):
        print("Invalid choice.")
        return

    cab = open_cabs[int(choice) - 1]
    boarded = cab.dispatch(pending)
    save_all(cabs, pending)

    print(f"\nDispatched: {cab.driver_name} -> {cab.destination} [{cab.time_slot}] "
          f"| Final Seats: {len(cab.students)}/{cab.seats}")
    if boarded:
        print("Newly boarded students (removed from waiting list):")
        for s in boarded:
            print(f"  - {s.student_name} (Year {s.year})")
    else:
        print("No new waiting students boarded.")


def main():
    cabs = load_cabs()
    pending = load_requests()
    actions = {"1": add_ride_request, "2": view_status, "3": find_matches, "4": dispatch_cab}

    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            save_all(cabs, pending)
            print("Data saved. Goodbye!")
            break
        if choice in actions:
            actions[choice](pending, cabs)
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()