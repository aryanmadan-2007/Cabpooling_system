from datetime import datetime

cities = ["Delhi", "Jaipur"]
time_slots = ["Morning", "Afternoon", "Evening", "Night"]


def check_choice(value, options, label):
    value = value.strip().title()
    if value not in options:
        raise ValueError(f"Invalid {label} '{value}'. Choose from: {', '.join(options)}.")
    return value


class RideRequest:
    def __init__(self, student_name, destination, time_slot, year, submitted_at=None):
        self.student_name = student_name.strip()
        if not self.student_name:
            raise ValueError("Student name cannot be empty.")
        if not 1 <= year <= 5:
            raise ValueError("Year must be between 1 and 5.")

        self.destination = check_choice(destination, cities, "destination")
        self.time_slot = check_choice(time_slot, time_slots, "time slot")
        self.year = year
        self.submitted_at = submitted_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return dict(vars(self))

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return (f"{self.student_name} (Year {self.year}) -> {self.destination} "
                f"[{self.time_slot}] | Submitted: {self.submitted_at}")


class Cab:
    def __init__(self, driver_name, seats, destination, time_slot, has_left=False, students=None):
        self.driver_name = driver_name.strip()
        if not self.driver_name:
            raise ValueError("Driver name cannot be empty.")
        if not 1 <= seats <= 4:
            raise ValueError("Seats must be between 1 and 4.")

        self.seats = seats
        self.destination = check_choice(destination, cities, "destination")
        self.time_slot = check_choice(time_slot, time_slots, "time slot")
        self.has_left = has_left
        self.students = students or []

    def to_dict(self):
        data = dict(vars(self))
        data["students"] = [s.to_dict() for s in self.students]
        return data

    @classmethod
    def from_dict(cls, data):
        data = dict(data)
        data["students"] = [RideRequest.from_dict(s) for s in data.get("students", [])]
        return cls(**data)

    def free_seats(self):
        return self.seats - len(self.students)

    def matches(self, requests):
        """Requests going the same place at the same time, up to the free seats."""
        same_trip = [r for r in requests
                     if r.destination == self.destination and r.time_slot == self.time_slot]
        return same_trip[:max(self.free_seats(), 0)]

    def dispatch(self, pending_requests):
        if self.has_left:
            raise ValueError(f"Cab driven by {self.driver_name} has already left.")

        boarded = self.matches(pending_requests)
        self.students.extend(boarded)
        for student in boarded:
            pending_requests.remove(student)

        self.has_left = True
        return boarded

    def __str__(self):
        status = "Already Left" if self.has_left else "Open"
        names = ", ".join(s.student_name for s in self.students) or "None"
        return (f"Driver: {self.driver_name} | {self.destination} ({self.time_slot}) | "
                f"Seats: {len(self.students)}/{self.seats} | Status: {status} | "
                f"Students: [{names}]")
