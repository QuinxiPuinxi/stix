class AircraftCalculator:
    def __init__(self, weight, surface_area, drag_coefficient):
        self.weight = weight  # in newtons
        self.surface_area = surface_area  # in square meters
        self.drag_coefficient = drag_coefficient

    def calculate_lift(self, air_density, velocity):
        """Calculate lift force using the lift equation."""
        lift = 0.5 * air_density * velocity**2 * self.surface_area
        return lift

    def calculate_drag(self, velocity):
        """Calculate drag force using the drag equation."""
        drag = 0.5 * self.drag_coefficient * velocity**2 * self.surface_area
        return drag

    def calculate_stability(self):
        """Check if the aircraft is stable based on weight and aerodynamic design."""
        # Simplified stability check, more complex models can be introduced
        return self.weight / self.surface_area < 1.0  # Placeholder condition
