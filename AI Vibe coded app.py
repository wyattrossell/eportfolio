"""
Student Grade Tracker - A GUI application for managing student names and grades.

Version: 1.0.1

This application allows the user to:
    - Add students and grades
    - Edit student names and individual grades
    - Delete students and individual grades
    - Sort students by name or average grade
    - Search for a student by name
    - Save and load student records to/from a JSON file
    - Toggle between a "Retro 80's Video Game" theme and a "Readable" theme

Dependencies:
    - Python 3.8+
    - tkinter (standard library)
    - json (standard library)
    - os (standard library)

Version 1.0.1 changes:
    - Fixed a crash on startup caused by the theming loop incorrectly matching
      the ttk.Combobox (sort dropdown) as a plain tk.Entry widget, since
      ttk.Combobox internally inherits from tkinter.Entry. The loop now checks
      the exact widget type instead of using isinstance(), and the Combobox is
      themed separately via ttk.Style.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os

# ---------------------------------------------------------------------------
# NAMED CONSTANTS
# ---------------------------------------------------------------------------

APP_TITLE = "Student Grade Tracker v1.0.1"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
DEFAULT_SAVE_FILE_NAME = "students.json"
JSON_FILE_TYPES = [("JSON files", "*.json"), ("All files", "*.*")]

# Sort mode constants
SORT_BY_NAME = "Name"
SORT_BY_AVERAGE = "Average Grade"

# Theme name constants
THEME_RETRO_80S = "Retro 80's Video Game"
THEME_READABLE = "Readable"

# Treeview column identifiers
COLUMN_NAME = "name"
COLUMN_GRADES = "grades"
COLUMN_AVERAGE = "average"

# Retro 80's Video Game theme colors and fonts
RETRO_BG_COLOR = "#000000"
RETRO_FG_COLOR = "#39FF14"          # neon green
RETRO_ACCENT_COLOR = "#FF00FF"      # neon magenta
RETRO_HIGHLIGHT_COLOR = "#00FFFF"   # neon cyan
RETRO_BUTTON_BG = "#1A1A1A"
RETRO_FONT_FAMILY = "Courier New"
RETRO_FONT_SIZE_NORMAL = 11
RETRO_FONT_SIZE_TITLE = 16

# Readable theme colors and fonts
READABLE_BG_COLOR = "#F5F5F5"
READABLE_FG_COLOR = "#000000"
READABLE_ACCENT_COLOR = "#004C99"
READABLE_HIGHLIGHT_COLOR = "#DDEBF7"
READABLE_BUTTON_BG = "#E0E0E0"
READABLE_FONT_FAMILY = "Segoe UI"
READABLE_FONT_SIZE_NORMAL = 11
READABLE_FONT_SIZE_TITLE = 16


# ---------------------------------------------------------------------------
# DATA MODEL: Student
# ---------------------------------------------------------------------------

class Student:
    """
    Represents a single student and their list of grades.
    """

    def __init__(self, name, grades=None):
        """
        Initialize a Student.

        Args:
            name (str): The student's name.
            grades (list[float], optional): An initial list of grades. Defaults to empty list.
        """
        self.name = name
        self.grades = grades if grades is not None else []

    def add_grade(self, grade):
        """Add a new grade to this student's list of grades."""
        self.grades.append(grade)

    def edit_grade(self, index, new_grade):
        """
        Replace the grade at the given index with a new value.

        Args:
            index (int): Index of the grade to replace.
            new_grade (float): The new grade value.

        Raises:
            IndexError: If the index is out of range.
        """
        self.grades[index] = new_grade

    def delete_grade(self, index):
        """
        Remove the grade at the given index.

        Args:
            index (int): Index of the grade to remove.

        Raises:
            IndexError: If the index is out of range.
        """
        del self.grades[index]

    def get_average_grade(self):
        """
        Calculate the average of all grades for this student.

        Returns:
            float: The average grade, or 0.0 if there are no grades.
        """
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def to_dict(self):
        """Convert this Student object into a JSON-serializable dictionary."""
        return {"name": self.name, "grades": self.grades}

    @staticmethod
    def from_dict(data):
        """
        Create a Student object from a dictionary (used when loading from JSON).

        Args:
            data (dict): Dictionary containing "name" and "grades" keys.

        Returns:
            Student: A newly constructed Student instance.
        """
        return Student(data["name"], data["grades"])


# ---------------------------------------------------------------------------
# DATA LAYER: StudentDatabase
# ---------------------------------------------------------------------------

class StudentDatabase:
    """
    Manages the full collection of Student objects, including CRUD operations,
    searching, sorting, and file persistence.
    """

    def __init__(self):
        """Initialize an empty student database."""
        self.students = []  # list[Student]

    def add_student(self, name):
        """
        Add a new student to the database.

        Args:
            name (str): The name of the new student.

        Returns:
            bool: True if added successfully, False if a student with that name already exists.
        """
        if self.find_student(name) is not None:
            return False
        self.students.append(Student(name))
        return True

    def delete_student(self, name):
        """
        Remove a student from the database by name.

        Args:
            name (str): Name of the student to remove.

        Returns:
            bool: True if a student was removed, False if not found.
        """
        student = self.find_student(name)
        if student is None:
            return False
        self.students.remove(student)
        return True

    def find_student(self, name):
        """
        Search for a student by exact name match.

        Args:
            name (str): Name to search for.

        Returns:
            Student or None: The matching Student object, or None if not found.
        """
        for student in self.students:
            if student.name == name:
                return student
        return None

    def search_students(self, partial_name):
        """
        Search for all students whose name contains the given substring (case-insensitive).

        Args:
            partial_name (str): Substring to search for.

        Returns:
            list[Student]: List of matching Student objects.
        """
        lowered_query = partial_name.lower()
        return [s for s in self.students if lowered_query in s.name.lower()]

    def edit_student_name(self, old_name, new_name):
        """
        Rename an existing student.

        Args:
            old_name (str): The student's current name.
            new_name (str): The student's new name.

        Returns:
            bool: True if the rename succeeded, False if old_name not found
                  or new_name is already taken by another student.
        """
        student = self.find_student(old_name)
        if student is None:
            return False
        if new_name != old_name and self.find_student(new_name) is not None:
            return False
        student.name = new_name
        return True

    def sort_students(self, sort_mode):
        """
        Sort the internal student list in place.

        Args:
            sort_mode (str): One of SORT_BY_NAME or SORT_BY_AVERAGE.
        """
        if sort_mode == SORT_BY_NAME:
            self.students.sort(key=lambda s: s.name.lower())
        elif sort_mode == SORT_BY_AVERAGE:
            self.students.sort(key=lambda s: s.get_average_grade(), reverse=True)

    def save_to_file(self, file_path):
        """
        Save all students to a JSON file.

        Args:
            file_path (str): Path to the file to write.
        """
        data = [student.to_dict() for student in self.students]
        with open(file_path, "w", encoding="utf-8") as file_handle:
            json.dump(data, file_handle, indent=4)

    def load_from_file(self, file_path):
        """
        Load students from a JSON file, replacing the current in-memory list.

        Args:
            file_path (str): Path to the file to read.
        """
        with open(file_path, "r", encoding="utf-8") as file_handle:
            data = json.load(file_handle)
        self.students = [Student.from_dict(item) for item in data]


# ---------------------------------------------------------------------------
# GUI LAYER: StudentGradeApp
# ---------------------------------------------------------------------------

class StudentGradeApp:
    """
    Main GUI application class. Builds and manages the tkinter window,
    widgets, and all user interaction event handlers.
    """

    def __init__(self, root):
        """
        Initialize the application.

        Args:
            root (tk.Tk): The root tkinter window.
        """
        self.root = root
        self.database = StudentDatabase()
        self.current_file_path = None
        self.current_theme = THEME_RETRO_80S  # Default style, as requested.

        self.root.title(APP_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self._build_widgets()
        self._apply_theme(self.current_theme)
        self._refresh_student_list()

    # -----------------------------------------------------------------
    # WIDGET CONSTRUCTION
    # -----------------------------------------------------------------

    def _build_widgets(self):
        """Construct and lay out all widgets in the main window."""

        # --- Top frame: title and theme toggle ---
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=(10, 0))

        self.title_label = tk.Label(self.top_frame, text="STUDENT GRADE TRACKER")
        self.title_label.pack(side="left")

        self.theme_button = tk.Button(
            self.top_frame, text="Toggle Style", command=self._on_toggle_theme
        )
        self.theme_button.pack(side="right")

        # --- Middle frame: student list (Treeview) ---
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.student_tree = ttk.Treeview(
            self.list_frame,
            columns=(COLUMN_NAME, COLUMN_GRADES, COLUMN_AVERAGE),
            show="headings",
            selectmode="browse",
        )
        self.student_tree.heading(COLUMN_NAME, text="Student Name")
        self.student_tree.heading(COLUMN_GRADES, text="Grades")
        self.student_tree.heading(COLUMN_AVERAGE, text="Average")
        self.student_tree.column(COLUMN_NAME, width=200)
        self.student_tree.column(COLUMN_GRADES, width=300)
        self.student_tree.column(COLUMN_AVERAGE, width=100, anchor="center")
        self.student_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            self.list_frame, orient="vertical", command=self.student_tree.yview
        )
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # --- Bottom frame: input fields ---
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill="x", padx=10, pady=(0, 5))

        tk.Label(self.input_frame, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(self.input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(self.input_frame, text="Grade:").grid(row=0, column=2, sticky="e")
        self.grade_entry = tk.Entry(self.input_frame, width=10)
        self.grade_entry.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(self.input_frame, text="Search:").grid(row=0, column=4, sticky="e")
        self.search_entry = tk.Entry(self.input_frame, width=20)
        self.search_entry.grid(row=0, column=5, padx=5, pady=3)

        self.sort_mode_var = tk.StringVar(value=SORT_BY_NAME)
        self.sort_dropdown = ttk.Combobox(
            self.input_frame,
            textvariable=self.sort_mode_var,
            values=[SORT_BY_NAME, SORT_BY_AVERAGE],
            state="readonly",
            width=15,
        )
        self.sort_dropdown.grid(row=0, column=6, padx=5, pady=3)

        # --- Button frame: action buttons ---
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(fill="x", padx=10, pady=(0, 10))

        button_definitions = [
            ("Add Student", self._on_add_student),
            ("Add Grade", self._on_add_grade),
            ("Edit Name", self._on_edit_name),
            ("Edit Grade", self._on_edit_grade),
            ("Delete Grade", self._on_delete_grade),
            ("Delete Student", self._on_delete_student),
            ("Sort", self._on_sort),
            ("Search", self._on_search),
            ("Show All", self._refresh_student_list),
            ("Save", self._on_save),
            ("Load", self._on_load),
        ]

        self.action_buttons = []
        for column_index, (button_text, callback) in enumerate(button_definitions):
            button = tk.Button(self.button_frame, text=button_text, command=callback)
            button.grid(row=0, column=column_index, padx=3, pady=3)
            self.action_buttons.append(button)

    # -----------------------------------------------------------------
    # THEME HANDLING
    # -----------------------------------------------------------------

    def _apply_theme(self, theme_name):
        """
        Apply the given theme's colors and fonts to every widget in the app.

        NOTE (fixed in v1.0.1): This method must distinguish plain tk widgets
        (which support -bg/-fg options) from ttk widgets (which do not, and
        must be styled via ttk.Style instead). ttk.Combobox internally
        inherits from tkinter.Entry, so a naive `isinstance(widget, tk.Entry)`
        check will incorrectly match it and crash when .configure(bg=...) is
        called on it. We use `type(widget) is tk.Entry` to require an exact
        type match instead.

        Args:
            theme_name (str): THEME_RETRO_80S or THEME_READABLE.
        """
        if theme_name == THEME_RETRO_80S:
            bg_color = RETRO_BG_COLOR
            fg_color = RETRO_FG_COLOR
            accent_color = RETRO_ACCENT_COLOR
            highlight_color = RETRO_HIGHLIGHT_COLOR
            button_bg = RETRO_BUTTON_BG
            font_family = RETRO_FONT_FAMILY
            font_size_normal = RETRO_FONT_SIZE_NORMAL
            font_size_title = RETRO_FONT_SIZE_TITLE
        else:
            bg_color = READABLE_BG_COLOR
            fg_color = READABLE_FG_COLOR
            accent_color = READABLE_ACCENT_COLOR
            highlight_color = READABLE_HIGHLIGHT_COLOR
            button_bg = READABLE_BUTTON_BG
            font_family = READABLE_FONT_FAMILY
            font_size_normal = READABLE_FONT_SIZE_NORMAL
            font_size_title = READABLE_FONT_SIZE_TITLE

        normal_font = (font_family, font_size_normal)
        title_font = (font_family, font_size_title, "bold")

        self.root.configure(bg=bg_color)
        self.top_frame.configure(bg=bg_color)
        self.list_frame.configure(bg=bg_color)
        self.input_frame.configure(bg=bg_color)
        self.button_frame.configure(bg=bg_color)

        self.title_label.configure(
            bg=bg_color, fg=accent_color, font=title_font
        )
        self.theme_button.configure(
            bg=button_bg, fg=fg_color, font=normal_font, activebackground=highlight_color
        )

        # Update plain tk labels/entries in the input frame.
        # IMPORTANT: use `type(widget) is X` (exact type check), NOT isinstance(),
        # because ttk.Combobox inherits from tkinter.Entry and would otherwise
        # be incorrectly matched here, causing a crash (ttk widgets don't
        # support the -bg/-fg configure options).
        for widget in self.input_frame.winfo_children():
            if type(widget) is tk.Label:
                widget.configure(bg=bg_color, fg=fg_color, font=normal_font)
            elif type(widget) is tk.Entry:
                widget.configure(
                    bg=button_bg, fg=fg_color, insertbackground=fg_color, font=normal_font
                )

        # Update all action buttons.
        for button in self.action_buttons:
            button.configure(
                bg=button_bg, fg=fg_color, font=normal_font, activebackground=highlight_color
            )

        # Update ttk-styled widgets (Treeview, Combobox) via a ttk.Style object.
        # ttk widgets ignore -bg/-fg entirely and must be themed this way.
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=button_bg,
            foreground=fg_color,
            fieldbackground=button_bg,
            font=normal_font,
        )
        style.configure(
            "Treeview.Heading",
            background=accent_color,
            foreground=bg_color if theme_name == THEME_RETRO_80S else fg_color,
            font=normal_font,
        )
        style.map("Treeview", background=[("selected", highlight_color)])

        # Theme the sort dropdown (ttk.Combobox) explicitly.
        style.configure(
            "TCombobox",
            fieldbackground=button_bg,
            background=button_bg,
            foreground=fg_color,
            arrowcolor=fg_color,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", button_bg)],
            foreground=[("readonly", fg_color)],
            background=[("readonly", button_bg)],
        )

        self.current_theme = theme_name

    def _on_toggle_theme(self):
        """Switch between the Retro 80's Video Game theme and the Readable theme."""
        new_theme = (
            THEME_READABLE if self.current_theme == THEME_RETRO_80S else THEME_RETRO_80S
        )
        self._apply_theme(new_theme)

    # -----------------------------------------------------------------
    # STUDENT LIST DISPLAY
    # -----------------------------------------------------------------

    def _refresh_student_list(self, students_to_show=None):
        """
        Repopulate the Treeview with the given list of students (or all students
        in the database if no list is provided).

        Args:
            students_to_show (list[Student], optional): Subset of students to display.
        """
        self.student_tree.delete(*self.student_tree.get_children())
        students = (
            students_to_show if students_to_show is not None else self.database.students
        )
        for student in students:
            grades_display = ", ".join(str(grade) for grade in student.grades)
            average_display = f"{student.get_average_grade():.2f}"
            self.student_tree.insert(
                "", "end", iid=student.name, values=(student.name, grades_display, average_display)
            )

    def _get_selected_student_name(self):
        """
        Get the name of the currently selected student in the Treeview.

        Returns:
            str or None: The selected student's name, or None if no selection.
        """
        selection = self.student_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a student from the list first.")
            return None
        return selection[0]

    # -----------------------------------------------------------------
    # EVENT HANDLERS: STUDENT / GRADE OPERATIONS
    # -----------------------------------------------------------------

    def _on_add_student(self):
        """Handle the 'Add Student' button: add a new student using the name entry field."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Invalid Name", "Please enter a student name.")
            return
        if not self.database.add_student(name):
            messagebox.showerror("Duplicate Name", f"A student named '{name}' already exists.")
            return
        self.name_entry.delete(0, tk.END)
        self._refresh_student_list()

    def _on_add_grade(self):
        """Handle the 'Add Grade' button: add the entered grade to the selected student."""
        student_name = self._get_selected_student_name()
        if student_name is None:
            return
        grade_value = self._parse_grade_entry()
        if grade_value is None:
            return
        student = self.database.find_student(student_name)
        student.add_grade(grade_value)
        self.grade_entry.delete(0, tk.END)
        self._refresh_student_list()

    def _on_edit_name(self):
        """Handle the 'Edit Name' button: rename the selected student."""
        student_name = self._get_selected_student_name()
        if student_name is None:
            return
        new_name = simpledialog.askstring(
            "Edit Name", "Enter new name:", initialvalue=student_name
        )
        if not new_name:
            return
        if not self.database.edit_student_name(student_name, new_name.strip()):
            messagebox.showerror("Error", "That name is already taken or the student was not found.")
            return
        self._refresh_student_list()

    def _on_edit_grade(self):
        """Handle the 'Edit Grade' button: edit a specific grade of the selected student."""
        student_name = self._get_selected_student_name()
        if student_name is None:
            return
        student = self.database.find_student(student_name)
        grade_index = self._prompt_for_grade_index(student)
        if grade_index is None:
            return
        new_grade_str = simpledialog.askstring(
            "Edit Grade", f"Enter new value for grade #{grade_index + 1}:"
        )
        if new_grade_str is None:
            return
        try:
            new_grade_value = float(new_grade_str)
        except ValueError:
            messagebox.showerror("Invalid Grade", "Grade must be a number.")
            return
        student.edit_grade(grade_index, new_grade_value)
        self._refresh_student_list()

    def _on_delete_grade(self):
        """Handle the 'Delete Grade' button: delete a specific grade from the selected student."""
        student_name = self._get_selected_student_name()
        if student_name is None:
            return
        student = self.database.find_student(student_name)
        grade_index = self._prompt_for_grade_index(student)
        if grade_index is None:
            return
        student.delete_grade(grade_index)
        self._refresh_student_list()

    def _on_delete_student(self):
        """Handle the 'Delete Student' button: remove the selected student entirely."""
        student_name = self._get_selected_student_name()
        if student_name is None:
            return
        confirmed = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete '{student_name}'?"
        )
        if not confirmed:
            return
        self.database.delete_student(student_name)
        self._refresh_student_list()

    def _on_sort(self):
        """Handle the 'Sort' button: sort the student list by the selected sort mode."""
        self.database.sort_students(self.sort_mode_var.get())
        self._refresh_student_list()

    def _on_search(self):
        """Handle the 'Search' button: filter the displayed list by the search entry text."""
        query = self.search_entry.get().strip()
        if not query:
            self._refresh_student_list()
            return
        matches = self.database.search_students(query)
        self._refresh_student_list(matches)

    # -----------------------------------------------------------------
    # EVENT HANDLERS: FILE OPERATIONS
    # -----------------------------------------------------------------

    def _on_save(self):
        """Handle the 'Save' button: save all student records to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=JSON_FILE_TYPES,
            initialfile=DEFAULT_SAVE_FILE_NAME,
        )
        if not file_path:
            return
        try:
            self.database.save_to_file(file_path)
            self.current_file_path = file_path
            messagebox.showinfo("Saved", f"Records saved to:\n{file_path}")
        except OSError as error:
            messagebox.showerror("Save Failed", f"Could not save file:\n{error}")

    def _on_load(self):
        """Handle the 'Load' button: load student records from a JSON file."""
        file_path = filedialog.askopenfilename(filetypes=JSON_FILE_TYPES)
        if not file_path:
            return
        try:
            self.database.load_from_file(file_path)
            self.current_file_path = file_path
            self._refresh_student_list()
            messagebox.showinfo("Loaded", f"Records loaded from:\n{file_path}")
        except (OSError, json.JSONDecodeError, KeyError) as error:
            messagebox.showerror("Load Failed", f"Could not load file:\n{error}")

    # -----------------------------------------------------------------
    # HELPER METHODS
    # -----------------------------------------------------------------

    def _parse_grade_entry(self):
        """
        Read and validate the grade entry field.

        Returns:
            float or None: The parsed grade value, or None if invalid (an error is shown).
        """
        grade_text = self.grade_entry.get().strip()
        try:
            return float(grade_text)
        except ValueError:
            messagebox.showerror("Invalid Grade", "Please enter a numeric grade.")
            return None

    def _prompt_for_grade_index(self, student):
        """
        Prompt the user to choose which grade (by 1-based position) to edit or delete.

        Args:
            student (Student): The student whose grades will be listed.

        Returns:
            int or None: The zero-based index of the chosen grade, or None if cancelled/invalid.
        """
        if not student.grades:
            messagebox.showinfo("No Grades", f"{student.name} has no grades yet.")
            return None
        grade_list_display = "\n".join(
            f"{index + 1}: {grade}" for index, grade in enumerate(student.grades)
        )
        choice = simpledialog.askstring(
            "Select Grade",
            f"Grades for {student.name}:\n{grade_list_display}\n\nEnter the number of the grade:",
        )
        if choice is None:
            return None
        try:
            chosen_index = int(choice) - 1
            if not (0 <= chosen_index < len(student.grades)):
                raise ValueError
            return chosen_index
        except ValueError:
            messagebox.showerror("Invalid Selection", "Please enter a valid grade number.")
            return None


# ---------------------------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    """Create the root tkinter window and launch the application."""
    root = tk.Tk()
    app = StudentGradeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()