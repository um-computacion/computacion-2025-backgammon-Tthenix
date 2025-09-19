class Player:
    TOTAL_CHECKERS = 15

    def __init__(self, name, color):
        if not name:
            raise ValueError("The name cannot be empty")

        color = color.lower()
        if color not in ("white", "black"):
            raise ValueError("Color should be 'white' o 'black'")

        self.name = name
        self.color = color
        self.checkers_count = self.TOTAL_CHECKERS
        self.captured_checkers = 0
        self.bear_off_count = 0

    def capture_checker(self):
        self.captured_checkers += 1
        if self.checkers_count > 0:
            self.checkers_count -= 1

    def release_captured_checker(self):
        if self.captured_checkers <= 0:
            raise ValueError("No captured checkers to release")
        self.captured_checkers -= 1
        self.checkers_count += 1

    def has_captured_checkers(self):
        return self.captured_checkers > 0

    def bear_off_checker(self):
        if self.checkers_count <= 0:
            raise ValueError("No checkers available for bear off")
        self.checkers_count -= 1
        self.bear_off_count += 1

    def can_bear_off(self):
        return self.checkers_count > 0

    def is_winner(self):
        return self.bear_off_count == self.TOTAL_CHECKERS

    def reset(self):
        self.checkers_count = self.TOTAL_CHECKERS
        self.captured_checkers = 0
        self.bear_off_count = 0

    def __str__(self):
        return f"{self.name} ({self.color}) - Checkers: {self.checkers_count}, Captured: {self.captured_checkers}, Bear off: {self.bear_off_count}"

    def __eq__(self, other):
        return isinstance(other, Player) and self.name == other.name and self.color == other.color

    def __hash__(self):
        return hash((self.name, self.color))