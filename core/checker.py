class Checker:
    TOTAL_POINTS = 24
    
    def __init__(self, color: str) -> None:
        """Initialize a checker with a specified color."""
        if color not in ("white", "black"):
            raise ValueError("Color must be 'white' or 'black'")
        self.color: str = color
        self.position: int | None = None
        self.is_on_bar: bool = False
        self.is_borne_off: bool = False

    def place_on_point(self, position: int) -> None:
        """Place the checker on a specific point on the board."""
        if position < 1 or position > self.TOTAL_POINTS:
            raise ValueError("Position must be between 1 and 24")
        
        self.position = position
        self.is_on_bar = False
        self.is_borne_off = False

    def move_to_point(self, position: int) -> None:
        """Move the checker to a specific point."""
        if self.is_borne_off:
            raise ValueError("Checker has already been removed from board")
        if self.is_on_bar:
            raise ValueError("Checker on bar cannot move directly")
        if self.position is None:
            raise ValueError("Checker must be placed before moving")
        if not (1 <= position <= self.TOTAL_POINTS):
            raise ValueError("Position must be between 1 and 24")
        
        self.position = position

    def send_to_bar(self) -> None:
        """Send the checker to the bar."""
        if self.is_on_bar:
            raise ValueError("Checker is already on bar")
        
        self.position = None
        self.is_on_bar = True
        self.is_borne_off = False

    def return_from_bar(self, position: int) -> None:
        """Return the checker from the bar to a specific point."""
        if not self.is_on_bar:
            raise ValueError("Checker is not on bar")
        if position < 1 or position > self.TOTAL_POINTS:
            raise ValueError("Position must be between 1 and 24")
        
        self.position = position
        self.is_on_bar = False
        self.is_borne_off = False

    def bear_off(self) -> None:
        """Remove the checker from the board (bear off)."""
        if self.is_borne_off:
            raise ValueError("Checker has already been removed from board")
        if self.is_on_bar:
            raise ValueError("Checker on bar cannot be borne off")
        if self.position is None:
            raise ValueError("Checker must be placed before bearing off")
        
        self.position = None
        self.is_on_bar = False
        self.is_borne_off = True
        
    def can_move(self) -> bool:
        """Check if the checker can move."""
        return (self.position is not None and 
                not self.is_on_bar and 
                not self.is_borne_off)

    def can_be_captured(self) -> bool:
        """Check if the checker can be captured."""
        return (self.position is not None and 
                not self.is_on_bar and 
                not self.is_borne_off)

    def reset(self) -> None:
        """Reset the checker to its initial state."""
        self.position = None
        self.is_on_bar = False
        self.is_borne_off = False

    def get_state(self) -> dict:
        """Get the current state of the checker."""
        return {
            'color': self.color,
            'position': self.position,
            'is_on_bar': self.is_on_bar,
            'is_borne_off': self.is_borne_off
        }

    def copy(self) -> 'Checker':
        """Create a copy of the checker."""
        new_checker = Checker(self.color)
        new_checker.position = self.position
        new_checker.is_on_bar = self.is_on_bar
        new_checker.is_borne_off = self.is_borne_off
        return new_checker

    def __str__(self) -> str:
        """String representation of the checker."""
        return (f"Checker(color={self.color}, position={self.position}, "
                f"on_bar={self.is_on_bar}, borne_off={self.is_borne_off})")

    def __eq__(self, other: object) -> bool:
        """Check equality with another checker."""
        if not isinstance(other, Checker):
            return False
        return (self.color == other.color and 
                self.position == other.position and
                self.is_on_bar == other.is_on_bar and
                self.is_borne_off == other.is_borne_off)

    def __hash__(self) -> int:
        """Generate hash for the checker."""
        return hash((self.color, self.position, self.is_on_bar, self.is_borne_off))