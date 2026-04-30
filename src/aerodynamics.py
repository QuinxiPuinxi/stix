# Aerodynamics Calculations for Yak-130 Aircraft

class Yak130Aerodynamics:
    def __init__(self):
        self.weight = 5200  # Weight in kg
        self.wing_area = 27.0  # Wing area in m²
        self.wing_span = 10.3  # Wing span in m
        self.drag_coefficient = 0.02  # Drag coefficient

    def lift_coefficient(self, angle_of_attack):
        # Simple lift coefficient based on angle of attack
        return 2 * 3.14 * angle_of_attack / 180  # converting angle to radians

    def lift_force(self, air_density, velocity, angle_of_attack):
        CL = self.lift_coefficient(angle_of_attack)
        return 0.5 * air_density * velocity**2 * self.wing_area * CL

    def drag_force(self, air_density, velocity):
        return 0.5 * air_density * velocity**2 * self.wing_area * self.drag_coefficient
