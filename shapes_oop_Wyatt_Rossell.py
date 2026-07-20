# shapes_oop.py
# Version 1.0
# Calculates the perimeter, area, and volume of several shapes and solids
# USING CLASSES AND INHERITANCE.
#
# Inheritance tree:
#   Shape
#    |__ Circle
#    |     |__ Cylinder      (a cylinder is built on a circular base)
#    |__ Rectangle
#    |     |__ Square        (a square is a special rectangle)
#    |     |__ Box           (a box is built on a rectangular base)
#    |__ Sphere
#
# 2D shapes report perimeter and area.
# 3D solids report surface area and volume.

import math


class Shape:
    """Base class for every shape and solid.

    Stores a name so each object can describe itself.  Child classes
    add the dimensions and the formulas that actually do the math.
    """

    def __init__(self, name):
        self.name = name

    def describe(self):
        """Return the name of the shape as a label."""
        return f"{self.name}"


# ---------------------------------------------------------------------------
# 2D SHAPES (perimeter and area)
# ---------------------------------------------------------------------------

class Circle(Shape):
    """A circle defined by its radius."""

    def __init__(self, radius):
        super().__init__("Circle")      # let the base class store the name
        self.radius = radius

    def perimeter(self):
        """Perimeter of a circle is its circumference: 2 * pi * r."""
        return 2 * math.pi * self.radius

    def area(self):
        """Area of a circle: pi * r^2."""
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    """A rectangle defined by its length and width."""

    def __init__(self, length, width, name="Rectangle"):
        super().__init__(name)          # name defaults to "Rectangle"
        self.length = length
        self.width = width

    def perimeter(self):
        """Perimeter of a rectangle: 2 * (length + width)."""
        return 2 * (self.length + self.width)

    def area(self):
        """Area of a rectangle: length * width."""
        return self.length * self.width


class Square(Rectangle):
    """A square is a rectangle whose length and width are equal.

    This class reuses ALL of Rectangle's math by passing the same value
    in for both the length and the width.
    """

    def __init__(self, side):
        # Reuse the Rectangle constructor with side used for both dimensions.
        super().__init__(side, side, name="Square")


# ---------------------------------------------------------------------------
# 3D SOLIDS (surface area and volume)
# ---------------------------------------------------------------------------

class Cylinder(Circle):
    """A cylinder is built on a circular base, so it inherits from Circle.

    It reuses the circle's area() method for the top and bottom circles.
    """

    def __init__(self, radius, height):
        super().__init__(radius)        # reuse the Circle constructor
        self.name = "Cylinder"          # override the inherited name
        self.height = height

    def surface_area(self):
        """Total surface area: two circular ends plus the side wall.

        The area() method is inherited from Circle (pi * r^2), so we
        reuse it here instead of writing the circle formula again.
        """
        two_ends = 2 * self.area()
        side_wall = 2 * math.pi * self.radius * self.height
        return two_ends + side_wall

    def volume(self):
        """Volume of a cylinder: base area * height."""
        return self.area() * self.height


class Box(Rectangle):
    """A rectangular box (right rectangular prism).

    It is built on a rectangular base, so it inherits from Rectangle and
    reuses that class's area() method for the base.
    """

    def __init__(self, length, width, height):
        super().__init__(length, width, name="Box")
        self.height = height

    def surface_area(self):
        """Total surface area: 2*(l*w) + 2*(l*h) + 2*(w*h).

        The l*w part is the base area, reused from Rectangle.area().
        """
        base = self.area()                          # length * width
        front_back = self.length * self.height
        left_right = self.width * self.height
        return 2 * base + 2 * front_back + 2 * left_right

    def volume(self):
        """Volume of a box: base area * height."""
        return self.area() * self.height


class Sphere(Shape):
    """A sphere defined by its radius."""

    def __init__(self, radius):
        super().__init__("Sphere")
        self.radius = radius

    def surface_area(self):
        """Surface area of a sphere: 4 * pi * r^2."""
        return 4 * math.pi * self.radius ** 2

    def volume(self):
        """Volume of a sphere: (4/3) * pi * r^3."""
        return (4 / 3) * math.pi * self.radius ** 3


# ---------------------------------------------------------------------------
# INPUT VALIDATION HELPER
# ---------------------------------------------------------------------------

def get_positive_float(prompt):
    """Keep asking until the user enters a number greater than zero.

    This performs BOTH kinds of checking the assignment asks for:
      - type checking  (must be a valid number, caught with try/except)
      - range checking (must be greater than zero)
    """
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("  Invalid entry. Please enter a number.")
            continue

        if value <= 0:
            print("  Value must be greater than zero. Please try again.")
            continue

        return value


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------

def main():
    print("Shape and Solid Calculator (OOP version)")
    print("========================================")

    keep_going = True
    while keep_going:
        print()
        print("Choose a shape or solid:")
        print("  1. Circle")
        print("  2. Rectangle")
        print("  3. Square")
        print("  4. Cylinder")
        print("  5. Box")
        print("  6. Sphere")
        print("  7. Quit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            radius = get_positive_float("Enter the radius: ")
            circle = Circle(radius)
            print(f"\n{circle.describe()}")
            print(f"  Perimeter (circumference): {circle.perimeter():,.2f}")
            print(f"  Area:                      {circle.area():,.2f}")

        elif choice == "2":
            length = get_positive_float("Enter the length: ")
            width = get_positive_float("Enter the width: ")
            rectangle = Rectangle(length, width)
            print(f"\n{rectangle.describe()}")
            print(f"  Perimeter: {rectangle.perimeter():,.2f}")
            print(f"  Area:      {rectangle.area():,.2f}")

        elif choice == "3":
            side = get_positive_float("Enter the side length: ")
            square = Square(side)
            print(f"\n{square.describe()}")
            print(f"  Perimeter: {square.perimeter():,.2f}")
            print(f"  Area:      {square.area():,.2f}")

        elif choice == "4":
            radius = get_positive_float("Enter the radius: ")
            height = get_positive_float("Enter the height: ")
            cylinder = Cylinder(radius, height)
            print(f"\n{cylinder.describe()}")
            print(f"  Surface area: {cylinder.surface_area():,.2f}")
            print(f"  Volume:       {cylinder.volume():,.2f}")

        elif choice == "5":
            length = get_positive_float("Enter the length: ")
            width = get_positive_float("Enter the width: ")
            height = get_positive_float("Enter the height: ")
            box = Box(length, width, height)
            print(f"\n{box.describe()}")
            print(f"  Surface area: {box.surface_area():,.2f}")
            print(f"  Volume:       {box.volume():,.2f}")

        elif choice == "6":
            radius = get_positive_float("Enter the radius: ")
            sphere = Sphere(radius)
            print(f"\n{sphere.describe()}")
            print(f"  Surface area: {sphere.surface_area():,.2f}")
            print(f"  Volume:       {sphere.volume():,.2f}")

        elif choice == "7":
            keep_going = False
            print("Goodbye!")

        else:
            print("  Invalid choice. Please enter a number from 1 to 7.")


main()