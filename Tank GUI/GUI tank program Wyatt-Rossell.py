"""
tank_gui.py
Version 2.0

A graphical (tkinter) version of the Water Tank Calculator.

The user enters the height and radius of an upright cylindrical tank
(a right circular cylinder) in feet.  The program then displays:

    - total volume in cubic feet
    - total volume in US gallons
    - total weight of the water in pounds
    - surface area of the top of the tank (square feet)
    - surface area of the outside/side of the tank (square feet)
    - total paintable area, top + side (square feet)

The user can also change the color scheme (four themes) and the window
size (three windowed sizes plus full screen) at any time while the
program is running.

CHANGELOG
    1.0  Console version.  Tank class plus text input/output.
    2.0  Added a tkinter GUI, four selectable color themes, selectable
         window sizes including full screen, live input validation with
         on-screen error messages, and a Clear button.

DESIGN NOTE - WHY THERE IS NO ttk IN THIS PROGRAM
    Only classic tkinter widgets (tk.Label, tk.Entry, tk.Button, ...) are
    used.  The themed ttk widgets do NOT accept the 'bg' and 'fg' options,
    so trying to recolor them raises a TclError at runtime.  Because a
    user-selectable color scheme is a required feature of this program,
    every widget must be recolorable, so classic tk widgets are used
    throughout.  tk.OptionMenu is used instead of ttk.Combobox for the
    same reason.

AUTHOR:  Wyatt Rossell
"""

import math
import tkinter as tk


# ---------------------------------------------------------------------------
# NAMED CONSTANTS
# ---------------------------------------------------------------------------

PROGRAM_TITLE = "Water Tank Calculator"
VERSION = "2.0"

# Unit conversion factors
GALLONS_PER_CUBIC_FOOT = 7.48052   # 1 cubic foot = 7.48052 US gallons
POUNDS_PER_CUBIC_FOOT = 62.4       # weight of fresh water per cubic foot

# Fonts used throughout the interface
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADING = ("Segoe UI", 11, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_RESULT = ("Consolas", 11)
FONT_STATUS = ("Segoe UI", 9, "italic")

# Available window sizes.  "Full Screen" is handled separately because it
# is set with an attribute rather than a geometry string.
WINDOW_SIZES = {
    "Small Window": "560x600",
    "Medium Window": "760x700",
    "Large Window": "1000x800",
    "Full Screen": "FULLSCREEN",
}
DEFAULT_WINDOW_SIZE = "Medium Window"

# Color schemes.  Every theme must define the same set of keys so that
# apply_theme() can rely on them being present.
#   bg          window and frame background
#   fg          normal text
#   accent      titles and section headings
#   entry_bg    background of the input boxes
#   entry_fg    text inside the input boxes
#   panel_bg    background of the results panel
#   button_bg   button background
#   button_fg   button text
#   error_fg    validation error message text
#   ok_fg       success message text
THEMES = {
    "Light": {
        "bg": "#f0f0f0", "fg": "#1c1c1c", "accent": "#1a4f8b",
        "entry_bg": "#ffffff", "entry_fg": "#1c1c1c", "panel_bg": "#ffffff",
        "button_bg": "#1a4f8b", "button_fg": "#ffffff",
        "error_fg": "#b00020", "ok_fg": "#1b6b2f",
    },
    "Dark": {
        "bg": "#1e1e1e", "fg": "#e6e6e6", "accent": "#4fa3ff",
        "entry_bg": "#2d2d2d", "entry_fg": "#e6e6e6", "panel_bg": "#252526",
        "button_bg": "#0e639c", "button_fg": "#ffffff",
        "error_fg": "#ff6b6b", "ok_fg": "#6bd68a",
    },
    "Ocean": {
        "bg": "#e8f4f8", "fg": "#13343b", "accent": "#00695c",
        "entry_bg": "#ffffff", "entry_fg": "#13343b", "panel_bg": "#d3ebf2",
        "button_bg": "#00838f", "button_fg": "#ffffff",
        "error_fg": "#c62828", "ok_fg": "#00695c",
    },
    "High Contrast": {
        "bg": "#000000", "fg": "#ffffff", "accent": "#ffff00",
        "entry_bg": "#000000", "entry_fg": "#ffff00", "panel_bg": "#000000",
        "button_bg": "#ffff00", "button_fg": "#000000",
        "error_fg": "#ff5555", "ok_fg": "#55ff55",
    },
}
DEFAULT_THEME = "Light"


# ---------------------------------------------------------------------------
# THE TANK CLASS  (unchanged logic from version 1.0 - no GUI code in here)
# ---------------------------------------------------------------------------

class Tank:
    """Represents an upright right circular cylinder (a water tank).

    The class stores only the two values the user supplies - the height
    and the radius, both in feet.  Everything else is calculated on
    demand by the methods below, so no derived value can ever fall out
    of step with the dimensions.

    Keeping this class free of any tkinter code means the exact same
    class could be reused by the console program, a web app, or a unit
    test without changing a single line.
    """

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
        """Return the area of the top of the tank in square feet.  A = pi * r^2"""
        return math.pi * self.radius ** 2

    def side_area(self):
        """Return the area of the outside wall in square feet.  A = 2 * pi * r * h"""
        return 2 * math.pi * self.radius * self.height

    def paint_area(self):
        """Return the total area to paint (top + side) in square feet."""
        return self.top_area() + self.side_area()


# ---------------------------------------------------------------------------
# THE GUI APPLICATION CLASS
# ---------------------------------------------------------------------------

class TankApp:
    """Builds and runs the tkinter interface for the Tank calculator.

    HOW THE THEMING WORKS
        As each widget is created it is added to one of the "role" lists
        below (frame_widgets, text_widgets, entry_widgets, ...).  When the
        user picks a new color scheme, apply_theme() simply walks those
        lists and recolors every widget according to its role.

        Registering widgets by role - rather than crawling the window and
        guessing at each widget's type - means a widget can never be given
        a color option it does not support, which is the usual cause of
        crashes in a theme switcher.
    """

    def __init__(self, root):
        """Set up the window, build the interface, and apply the defaults."""
        self.root = root
        self.root.title(f"{PROGRAM_TITLE} v{VERSION}")
        self.root.minsize(480, 560)

        # Current user preferences, held in tkinter control variables so the
        # menus and drop-downs stay in sync with each other automatically.
        self.theme_name = tk.StringVar(value=DEFAULT_THEME)
        self.size_name = tk.StringVar(value=DEFAULT_WINDOW_SIZE)

        # Role lists used by apply_theme().  Every widget gets registered in
        # exactly one of these as it is created.
        self.frame_widgets = []    # frames and the root window
        self.text_widgets = []     # ordinary labels
        self.heading_widgets = []  # titles and section headings (accent color)
        self.entry_widgets = []    # input boxes
        self.button_widgets = []   # buttons
        self.panel_widgets = []    # frames that make up the results panel
        self.panel_text = []       # labels sitting on the results panel
        self.option_widgets = []   # OptionMenu drop-downs

        # Build the interface.
        self._build_menu_bar()
        self._build_control_bar()
        self._build_input_section()
        self._build_button_section()
        self._build_results_section()
        self._build_status_bar()

        # Apply the starting theme and window size.
        self.apply_theme(DEFAULT_THEME)
        self.set_window_size(DEFAULT_WINDOW_SIZE)

        # Convenience key bindings.
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.exit_full_screen())

    # -- interface construction --------------------------------------------

    def _build_menu_bar(self):
        """Create the drop-down menu bar across the top of the window.

        The menu bar gives a second, more conventional way to reach the
        same theme and window-size settings offered by the control bar.
        """
        menu_bar = tk.Menu(self.root)

        # View menu, with a submenu for each setting.
        view_menu = tk.Menu(menu_bar, tearoff=0)

        theme_menu = tk.Menu(view_menu, tearoff=0)
        for name in THEMES:
            # A radiobutton entry shows a dot beside the active theme.
            theme_menu.add_radiobutton(
                label=name,
                variable=self.theme_name,
                value=name,
                command=lambda n=name: self.apply_theme(n),
            )
        view_menu.add_cascade(label="Color Scheme", menu=theme_menu)

        size_menu = tk.Menu(view_menu, tearoff=0)
        for name in WINDOW_SIZES:
            size_menu.add_radiobutton(
                label=name,
                variable=self.size_name,
                value=name,
                command=lambda n=name: self.set_window_size(n),
            )
        view_menu.add_cascade(label="Window Size", menu=size_menu)

        view_menu.add_separator()
        view_menu.add_command(label="Exit Full Screen (Esc)",
                              command=self.exit_full_screen)
        menu_bar.add_cascade(label="View", menu=view_menu)

        # File menu.
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Clear", command=self.clear)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def _build_control_bar(self):
        """Create the on-screen theme and window-size drop-downs.

        These do exactly the same job as the View menu.  They are placed in
        the window itself so the settings are visible and obvious rather
        than hidden inside a menu.
        """
        bar = tk.Frame(self.root, padx=12, pady=8)
        bar.pack(fill="x")
        self.frame_widgets.append(bar)

        theme_label = tk.Label(bar, text="Color scheme:", font=FONT_LABEL)
        theme_label.pack(side="left")
        self.text_widgets.append(theme_label)

        # tk.OptionMenu is used instead of ttk.Combobox because, unlike the
        # ttk version, it accepts the bg/fg options this program needs.
        theme_picker = tk.OptionMenu(bar, self.theme_name, *THEMES.keys(),
                                     command=self.apply_theme)
        theme_picker.config(font=FONT_LABEL, width=12, relief="flat")
        theme_picker.pack(side="left", padx=(6, 20))
        self.option_widgets.append(theme_picker)

        size_label = tk.Label(bar, text="Window:", font=FONT_LABEL)
        size_label.pack(side="left")
        self.text_widgets.append(size_label)

        size_picker = tk.OptionMenu(bar, self.size_name, *WINDOW_SIZES.keys(),
                                    command=self.set_window_size)
        size_picker.config(font=FONT_LABEL, width=13, relief="flat")
        size_picker.pack(side="left", padx=6)
        self.option_widgets.append(size_picker)

    def _build_input_section(self):
        """Create the title and the two input boxes."""
        title = tk.Label(self.root, text=PROGRAM_TITLE, font=FONT_TITLE)
        title.pack(pady=(4, 2))
        self.heading_widgets.append(title)

        subtitle = tk.Label(
            self.root,
            text="Enter the dimensions of an upright cylindrical tank, in feet.",
            font=FONT_LABEL,
        )
        subtitle.pack(pady=(0, 10))
        self.text_widgets.append(subtitle)

        form = tk.Frame(self.root, padx=20)
        form.pack(fill="x")
        self.frame_widgets.append(form)

        # Height row.
        height_label = tk.Label(form, text="Height (feet):", font=FONT_LABEL,
                                width=14, anchor="w")
        height_label.grid(row=0, column=0, sticky="w", pady=6)
        self.text_widgets.append(height_label)

        self.height_entry = tk.Entry(form, font=FONT_LABEL, relief="solid", bd=1)
        self.height_entry.grid(row=0, column=1, sticky="ew", pady=6, ipady=4)
        self.entry_widgets.append(self.height_entry)

        # Radius row.
        radius_label = tk.Label(form, text="Radius (feet):", font=FONT_LABEL,
                                width=14, anchor="w")
        radius_label.grid(row=1, column=0, sticky="w", pady=6)
        self.text_widgets.append(radius_label)

        self.radius_entry = tk.Entry(form, font=FONT_LABEL, relief="solid", bd=1)
        self.radius_entry.grid(row=1, column=1, sticky="ew", pady=6, ipady=4)
        self.entry_widgets.append(self.radius_entry)

        # Let column 1 (the entry boxes) absorb any extra width when the
        # window is resized or maximized.
        form.columnconfigure(1, weight=1)

    def _build_button_section(self):
        """Create the Calculate and Clear buttons."""
        buttons = tk.Frame(self.root, pady=12)
        buttons.pack()
        self.frame_widgets.append(buttons)

        calc_button = tk.Button(buttons, text="Calculate", font=FONT_HEADING,
                                width=14, relief="flat", cursor="hand2",
                                command=self.calculate)
        calc_button.pack(side="left", padx=6, ipady=4)
        self.button_widgets.append(calc_button)

        clear_button = tk.Button(buttons, text="Clear", font=FONT_HEADING,
                                 width=10, relief="flat", cursor="hand2",
                                 command=self.clear)
        clear_button.pack(side="left", padx=6, ipady=4)
        self.button_widgets.append(clear_button)

    def _build_results_section(self):
        """Create the panel that displays the six calculated results.

        Each result gets a description label on the left and a value label
        on the right.  The value labels are stored in self.result_values so
        that calculate() and clear() can update their text later.
        """
        panel = tk.Frame(self.root, padx=16, pady=12, relief="solid", bd=1)
        panel.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.panel_widgets.append(panel)

        # The six outputs, in display order.  The key is used to look the
        # value label back up when the results are filled in.
        result_rows = [
            ("volume_cf", "Total volume:", "cubic feet"),
            ("volume_gal", "Total volume:", "gallons"),
            ("weight", "Weight of water:", "pounds"),
            ("top_area", "Top surface area:", "square feet"),
            ("side_area", "Side surface area:", "square feet"),
            ("paint_area", "Total area to paint:", "square feet"),
        ]

        heading = tk.Label(panel, text="Results", font=FONT_HEADING, anchor="w")
        heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))
        self.heading_widgets.append(heading)

        self.result_values = {}    # key -> the Label that shows the number

        for row_number, (key, description, unit) in enumerate(result_rows, start=1):
            # A blank line before the surface-area group keeps the two
            # groups of results visually separate.
            pad_top = 10 if key == "top_area" else 2

            desc_label = tk.Label(panel, text=description, font=FONT_LABEL,
                                  anchor="w")
            desc_label.grid(row=row_number, column=0, sticky="w",
                            pady=(pad_top, 2))
            self.panel_text.append(desc_label)

            value_label = tk.Label(panel, text="--", font=FONT_RESULT,
                                   anchor="e", width=14)
            value_label.grid(row=row_number, column=1, sticky="e",
                             padx=10, pady=(pad_top, 2))
            self.panel_text.append(value_label)
            self.result_values[key] = value_label

            unit_label = tk.Label(panel, text=unit, font=FONT_LABEL, anchor="w")
            unit_label.grid(row=row_number, column=2, sticky="w",
                            pady=(pad_top, 2))
            self.panel_text.append(unit_label)

        # Let the middle column stretch so the numbers stay right-aligned
        # against the units when the window grows.
        panel.columnconfigure(1, weight=1)

    def _build_status_bar(self):
        """Create the message line at the bottom of the window.

        This is where validation errors are reported.  Showing the error in
        the window itself - rather than a pop-up box that must be dismissed -
        keeps the user's place in the form.
        """
        self.status_label = tk.Label(self.root, text="Ready.", font=FONT_STATUS,
                                     anchor="w", padx=12, pady=6)
        self.status_label.pack(fill="x", side="bottom")
        self.text_widgets.append(self.status_label)

    # -- appearance settings -----------------------------------------------

    def apply_theme(self, theme_name):
        """Recolor every widget in the window to the chosen color scheme.

        Walks the role lists that were built during construction and gives
        each widget only the color options that its role actually supports.
        """
        theme = THEMES[theme_name]
        self.theme_name.set(theme_name)

        # The window itself.
        self.root.config(bg=theme["bg"])

        for widget in self.frame_widgets:
            widget.config(bg=theme["bg"])

        for widget in self.text_widgets:
            widget.config(bg=theme["bg"], fg=theme["fg"])

        for widget in self.heading_widgets:
            widget.config(bg=theme["bg"], fg=theme["accent"])

        for widget in self.entry_widgets:
            widget.config(bg=theme["entry_bg"], fg=theme["entry_fg"],
                          insertbackground=theme["entry_fg"])

        for widget in self.button_widgets:
            widget.config(bg=theme["button_bg"], fg=theme["button_fg"],
                          activebackground=theme["accent"],
                          activeforeground=theme["button_fg"])

        for widget in self.panel_widgets:
            widget.config(bg=theme["panel_bg"])

        for widget in self.panel_text:
            widget.config(bg=theme["panel_bg"], fg=theme["fg"])

        # An OptionMenu is really two widgets: the button the user sees and
        # the pop-up menu it opens.  Both have to be recolored.
        for widget in self.option_widgets:
            widget.config(bg=theme["entry_bg"], fg=theme["entry_fg"],
                          activebackground=theme["accent"],
                          activeforeground=theme["button_fg"],
                          highlightthickness=0)
            widget["menu"].config(bg=theme["entry_bg"], fg=theme["entry_fg"])

        # The headings inside the results panel sit on the panel background,
        # not the window background, so they are corrected here.
        self.result_heading_fix(theme)

        # Repaint the status line in the right color for its current message.
        self.status_label.config(bg=theme["bg"])

    def result_heading_fix(self, theme):
        """Put the 'Results' heading on the panel background, not the window.

        The heading was registered as a heading widget so it would pick up
        the accent color, but it physically sits on the results panel, so
        its background has to be corrected after the main theming pass.
        """
        for widget in self.heading_widgets:
            if widget.cget("text") == "Results":
                widget.config(bg=theme["panel_bg"], fg=theme["accent"])

    def set_window_size(self, size_name):
        """Switch between the windowed sizes and full screen."""
        self.size_name.set(size_name)
        geometry = WINDOW_SIZES[size_name]

        if geometry == "FULLSCREEN":
            self.root.attributes("-fullscreen", True)
            self.set_status("Full screen. Press Esc to return to a window.", "ok")
        else:
            # Leaving full screen first, otherwise the geometry request is
            # ignored while the window is still full screen.
            self.root.attributes("-fullscreen", False)
            self.root.geometry(geometry)

    def exit_full_screen(self):
        """Leave full screen and return to the default windowed size.

        Bound to the Escape key so the user is never trapped in full screen.

        Two conditions are checked rather than one.  Asking the window
        manager whether the window is full screen is the obvious test, but
        the program's own setting is checked as well so that the drop-down
        can never be left displaying "Full Screen" while the window is not.
        Pressing Escape in an ordinary window does nothing, which is what
        the user would expect.
        """
        is_full_screen = bool(self.root.attributes("-fullscreen"))
        setting_says_full = self.size_name.get() == "Full Screen"

        if is_full_screen or setting_says_full:
            self.set_window_size(DEFAULT_WINDOW_SIZE)
            self.set_status("Ready.", "normal")

    def set_status(self, message, kind="normal"):
        """Display a message on the status line.

        kind is "normal", "error", or "ok", and selects the text color from
        the active theme.
        """
        theme = THEMES[self.theme_name.get()]
        color = {
            "error": theme["error_fg"],
            "ok": theme["ok_fg"],
            "normal": theme["fg"],
        }[kind]
        self.status_label.config(text=message, fg=color, bg=theme["bg"])

    # -- input validation ---------------------------------------------------

    def validate_dimension(self, text, field_name):
        """Check one input box and convert it to a number.

        Returns the value as a float if it is acceptable.  Returns None and
        posts an error message if it is not.  Performs all three checks the
        program needs:

            presence   - the box must not be empty
            type       - the text must convert to a number
            range      - the number must be greater than zero

        A tank cannot have a zero or negative dimension, so zero and
        negatives are rejected rather than silently producing a meaningless
        answer.
        """
        text = text.strip()

        if text == "":
            self.set_status(f"Please enter a {field_name}.", "error")
            return None

        try:
            value = float(text)
        except ValueError:
            self.set_status(f"The {field_name} must be a number.", "error")
            return None

        if value <= 0:
            self.set_status(f"The {field_name} must be greater than zero.",
                            "error")
            return None

        return value

    # -- actions ------------------------------------------------------------

    def calculate(self):
        """Validate the inputs, build a Tank, and display the six results."""
        height = self.validate_dimension(self.height_entry.get(), "height")
        if height is None:
            self.clear_results()
            self.height_entry.focus_set()
            return

        radius = self.validate_dimension(self.radius_entry.get(), "radius")
        if radius is None:
            self.clear_results()
            self.radius_entry.focus_set()
            return

        # Both inputs are good, so the Tank object can be created safely.
        tank = Tank(height, radius)

        self.result_values["volume_cf"].config(
            text=f"{tank.volume_cubic_feet():,.2f}")
        self.result_values["volume_gal"].config(
            text=f"{tank.volume_gallons():,.2f}")
        self.result_values["weight"].config(
            text=f"{tank.water_weight_pounds():,.2f}")
        self.result_values["top_area"].config(
            text=f"{tank.top_area():,.2f}")
        self.result_values["side_area"].config(
            text=f"{tank.side_area():,.2f}")
        self.result_values["paint_area"].config(
            text=f"{tank.paint_area():,.2f}")

        self.set_status(
            f"Calculated for a tank {height:,.2f} ft tall "
            f"with a {radius:,.2f} ft radius.", "ok")

    def clear_results(self):
        """Blank out the six result values without touching the inputs."""
        for value_label in self.result_values.values():
            value_label.config(text="--")

    def clear(self):
        """Empty the input boxes and the results, ready for a new tank."""
        self.height_entry.delete(0, tk.END)
        self.radius_entry.delete(0, tk.END)
        self.clear_results()
        self.set_status("Ready.", "normal")
        self.height_entry.focus_set()


# ---------------------------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------------------------

def main():
    """Create the main window, start the application, and run it."""
    root = tk.Tk()
    app = TankApp(root)
    app.height_entry.focus_set()
    root.mainloop()


main()