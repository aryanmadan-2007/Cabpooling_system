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

        self.destination = check_choice(destination, cities, "destination")
        self.time_slot = check_choice(time_slot, time_slots, "time slot")

        if year not in range(1, 6):
            raise ValueError("Year must be a number between 1 and 5.")
        self.year = year

        # Keep the saved time when loading from file, otherwise use now
        self.submitted_at = submitted_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return (f"{self.student_name} (Year {self.year}) -> {self.destination} "
                f"[{self.time_slot}] | Submitted: {self.submitted_at}")


class Cab:
    def __init__(self, driver_name, seats, destination, time_slot, has_left=False):
        self.driver_name = driver_name.strip()
        if not self.driver_name:
            raise ValueError("Driver name cannot be empty.")

        if seats not in range(1, 5):
            raise ValueError("Seats must be between 1 and 4.")
        self.seats = seats

        self.destination = check_choice(destination, cities, "destination")
        self.time_slot = check_choice(time_slot, time_slots, "time slot")
        self.has_left = has_left

    def to_dict(self):
        return vars(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        status = "Already Left" if self.has_left else "Open"
        return (f"Driver: {self.driver_name} | {self.destination} ({self.time_slot}) | "
                f"Seats: {self.seats} | Status: {status}")
