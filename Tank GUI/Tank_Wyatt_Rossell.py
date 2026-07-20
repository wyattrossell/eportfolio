# tank.py
# Version 1.0
# A program that models an upright cylindrical water tank.
# The Tank class stores only the height and radius (in feet) and
# calculates volume, weight of water, and paintable surface areas.

import math

# Named constants (conversion factors)
GALLONS_PER_CUBIC_FOOT = 7.48052   # 1 cubic foot = 7.48052 US gallons
POUNDS_PER_CUBIC_FOOT = 62.4       # weight of fresh water per cubic foot


class Tank:
    """Represents an upright right circular cylinder (a water tank)."""

    def __init__(self, height, radius):
        """Initialize the tank with a height and radius, both in feet."""
        self.height = height
        self.radius = radius

    def volume_cubic_feet(self):
        """Return the total volume in cubic feet.  V = pi * r^2 * h"""
        return math.pi * self.radius ** 2 * self.height

    def volume_gallons(self):
        """Return the total volume in US gallons."""
        return self.volume_cubic_feet() * GALLONS_PER_CUBIC_FOOT

    def water_weight_pounds(self):
        """Return the weight of the water in pounds when the tank is full."""
        return self.volume_cubic_feet() * POUNDS_PER_CUBIC_FOOT

    def top_area(self):
        """Return the surface area of the top of the tank in square feet.
        A = pi * r^2"""
        return math.pi * self.radius ** 2

    def side_area(self):
        """Return the surface area of the outside (side wall) of the tank
        in square feet.  A = 2 * pi * r * h"""
        return 2 * math.pi * self.radius * self.height

    def paint_area(self):
        """Return the total area to paint (top + side) in square feet."""
        return self.top_area() + self.side_area()


def main():
    print("Water Tank Calculator")
    print("---------------------")

    # Get the tank dimensions from the user, with error checking
    try:
        height = float(input("Enter the height of the tank in feet: "))
        radius = float(input("Enter the radius of the tank in feet: "))
    except ValueError:
        print("Error: height and radius must be numbers.")
        return

    if height <= 0 or radius <= 0:
        print("Error: height and radius must be greater than zero.")
        return

    # Create the tank object
    tank = Tank(height, radius)

    # Display the results
    print()
    print(f"Total volume:        {tank.volume_cubic_feet():,.2f} cubic feet")
    print(f"Total volume:        {tank.volume_gallons():,.2f} gallons")
    print(f"Weight of water:     {tank.water_weight_pounds():,.2f} pounds")
    print()
    print(f"Top surface area:    {tank.top_area():,.2f} square feet")
    print(f"Side surface area:   {tank.side_area():,.2f} square feet")
    print(f"Total area to paint: {tank.paint_area():,.2f} square feet")


main()