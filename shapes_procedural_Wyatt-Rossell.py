# shapes_procedural.py
# Version 1.0
# Calculates the perimeter, area, and volume of several shapes and solids
# WITHOUT using classes or inheritance.
#
# Every shape is handled by plain functions that take the dimensions as
# arguments and return a number.  There are no objects and no inheritance,
# so shapes that share math (like a square and a rectangle) reuse code by
# CALLING another function rather than inheriting from it.
#
# 2D shapes report perimeter and area.
# 3D solids report surface area and volume.

import math


# ---------------------------------------------------------------------------
# 2D SHAPE FORMULAS (perimeter and area)
# ---------------------------------------------------------------------------

def circle_circumference(radius):
    """Perimeter (circumference) of a circle: 2 * pi * r."""
    return 2 * math.pi * radius


def circle_area(radius):
    """Area of a circle: pi * r^2."""
    return math.pi * radius ** 2


def rectangle_perimeter(length, width):
    """Perimeter of a rectangle: 2 * (length + width)."""
    return 2 * (length + width)


def rectangle_area(length, width):
    """Area of a rectangle: length * width."""
    return length * width


def square_perimeter(side):
    """Perimeter of a square.

    A square is just a rectangle with equal sides, so we reuse the
    rectangle function by passing the side in for both dimensions.
    Without inheritance, this call is how we avoid duplicating the math.
    """
    return rectangle_perimeter(side, side)


def square_area(side):
    """Area of a square, reusing the rectangle area function."""
    return rectangle_area(side, side)


# ---------------------------------------------------------------------------
# 3D SOLID FORMULAS (surface area and volume)
# ---------------------------------------------------------------------------

def cylinder_surface_area(radius, height):
    """Total surface area of a cylinder: two ends plus the side wall.

    We reuse circle_area() for the two circular ends.
    """
    two_ends = 2 * circle_area(radius)
    side_wall = 2 * math.pi * radius * height
    return two_ends + side_wall


def cylinder_volume(radius, height):
    """Volume of a cylinder: base area * height (reuses circle_area)."""
    return circle_area(radius) * height


def box_surface_area(length, width, height):
    """Total surface area of a box: 2*(l*w) + 2*(l*h) + 2*(w*h)."""
    base = rectangle_area(length, width)        # reuse rectangle area
    front_back = length * height
    left_right = width * height
    return 2 * base + 2 * front_back + 2 * left_right


def box_volume(length, width, height):
    """Volume of a box: base area * height (reuses rectangle_area)."""
    return rectangle_area(length, width) * height


def sphere_surface_area(radius):
    """Surface area of a sphere: 4 * pi * r^2."""
    return 4 * math.pi * radius ** 2


def sphere_volume(radius):
    """Volume of a sphere: (4/3) * pi * r^3."""
    return (4 / 3) * math.pi * radius ** 3


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
    print("Shape and Solid Calculator (procedural version)")
    print("===============================================")

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
            print("\nCircle")
            print(f"  Perimeter (circumference): {circle_circumference(radius):,.2f}")
            print(f"  Area:                      {circle_area(radius):,.2f}")

        elif choice == "2":
            length = get_positive_float("Enter the length: ")
            width = get_positive_float("Enter the width: ")
            print("\nRectangle")
            print(f"  Perimeter: {rectangle_perimeter(length, width):,.2f}")
            print(f"  Area:      {rectangle_area(length, width):,.2f}")

        elif choice == "3":
            side = get_positive_float("Enter the side length: ")
            print("\nSquare")
            print(f"  Perimeter: {square_perimeter(side):,.2f}")
            print(f"  Area:      {square_area(side):,.2f}")

        elif choice == "4":
            radius = get_positive_float("Enter the radius: ")
            height = get_positive_float("Enter the height: ")
            print("\nCylinder")
            print(f"  Surface area: {cylinder_surface_area(radius, height):,.2f}")
            print(f"  Volume:       {cylinder_volume(radius, height):,.2f}")

        elif choice == "5":
            length = get_positive_float("Enter the length: ")
            width = get_positive_float("Enter the width: ")
            height = get_positive_float("Enter the height: ")
            print("\nBox")
            print(f"  Surface area: {box_surface_area(length, width, height):,.2f}")
            print(f"  Volume:       {box_volume(length, width, height):,.2f}")

        elif choice == "6":
            radius = get_positive_float("Enter the radius: ")
            print("\nSphere")
            print(f"  Surface area: {sphere_surface_area(radius):,.2f}")
            print(f"  Volume:       {sphere_volume(radius):,.2f}")

        elif choice == "7":
            keep_going = False
            print("Goodbye!")

        else:
            print("  Invalid choice. Please enter a number from 1 to 7.")


main()