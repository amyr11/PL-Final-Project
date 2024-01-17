import tkinter.messagebox as messagebox
from utils.database import Database
import customtkinter as ctk
from tkinter import ttk


class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.grid_columnconfigure(0, weight=1)

        # Form widgets
        self.title_frame = ctk.CTkFrame(self)
        self.title_label = ctk.CTkLabel(
            self.title_frame, text="Office of the University Registrar", font=("", 24)
        )
        self.title_label.pack(padx=40, pady=(10, 0))
        self.subtitle_label = ctk.CTkLabel(
            self.title_frame, text="Inquiry System", font=("", 16)
        )
        self.subtitle_label.pack(padx=20, pady=(0, 20))

        self.employee_number_label = ctk.CTkLabel(self, text="Employee Number")
        self.employee_number_entry = ctk.CTkEntry(self)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_entry = ctk.CTkEntry(self, show="*")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)

        # Grid layout
        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.employee_number_label.grid(
            row=1, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.employee_number_entry.grid(row=2, column=0, padx=10, sticky="ew")

        self.password_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.password_entry.grid(row=4, column=0, padx=10, sticky="ew")

        self.login_button.grid(
            row=5, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew"
        )

    def login(self):
        employee_number = self.employee_number_entry.get()
        password = self.password_entry.get()

        # Validate the data
        if not (employee_number and password):
            messagebox.showwarning(
                "Missing Fields", "Please fill out both fields before logging in."
            )
            return

        if not employee_number.isdigit() and len(employee_number) != 9:
            messagebox.showwarning(
                "Invalid Employee Number",
                "Please enter a valid employee number.",
            )
            return

        # Check the login credentials against the database
        db = Database()
        if db.verify_login(employee_number, password):
            self.withdraw()  # Close the login window
            main_window = MainWindow(self)
            main_window.show()
        else:
            messagebox.showwarning(
                "Invalid Credentials", "Invalid employee number or password."
            )


class MainWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Main Window")
        self.geometry("1070x640")
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=18, pady=(0, 18), fill="both", expand=True)

        self.students_tab = self.tabview.add("Students")
        self.grades_tab = self.tabview.add("Grades")
        self.documents_tab = self.tabview.add("Document Requests")
        self.sms_tab = self.tabview.add("Bulk SMS")

        self.students_tab_view = StudentsTab(self.students_tab)
        self.grades_tab_view = GradesTab(self.grades_tab)
        self.documents_tab_view = DocumentsTab(self.documents_tab)
        self.sms_tab_view = SMSTab(self.sms_tab)

        self.students_tab_view.pack(fill="both", expand=True)
        self.grades_tab_view.pack(fill="both", expand=True)
        self.documents_tab_view.pack(fill="both", expand=True)
        self.sms_tab_view.pack(fill="both", expand=True)

    def show(self):
        self.wait_visibility()  # Ensure the window is visible
        self.grab_set()  # Make this window modal
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event
        self.focus_set()  # Set focus to this window

    def on_close(self):
        self.grab_release()  # Release the modal state
        self.destroy()  # Close the main window
        self.master.destroy()  # Show the login window again


class StudentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Widgets
        self.students_table = ttk.Treeview(
            self,
            columns=(
                "student_number",
                "firstname",
                "middlename",
                "lastname",
                "year_level",
                "email",
                "contact_number",
                "course_code",
            ),
            show="headings",
            selectmode="extended",
        )
        self.students_table.heading("student_number", text="Student no.")
        self.students_table.heading("firstname", text="First name")
        self.students_table.heading("middlename", text="Middle name")
        self.students_table.heading("lastname", text="Last name")
        self.students_table.heading("year_level", text="Year level")
        self.students_table.heading("email", text="Email")
        self.students_table.heading("contact_number", text="Contact number")
        self.students_table.heading("course_code", text="Course code")

        self.populate_students_table()

        s = ttk.Style()
        s.configure("Treeview", rowheight=25)

        self.search_frame = ctk.CTkFrame(self)
        self.search_bar = ctk.CTkEntry(
            self.search_frame, placeholder_text="Enter student no."
        )
        self.search_button = ctk.CTkButton(
            self.search_frame, text="🔍 Search", command=self.search, width=40
        )
        self.reset_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            command=self.reset_table,
            fg_color="grey",
            width=20,
        )

        # Grid layout
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.search_bar.grid(row=0, column=0, sticky="w")
        self.search_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.reset_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.students_table.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def populate_students_table(self, students=None):
        if not students:
            db = Database()
            students = db.get_all("student_info")

        self.students_table.delete(*self.students_table.get_children())

        for student in students:
            self.students_table.insert(
                "",
                "end",
                values=(
                    student["student_id"],
                    student["first_name"],
                    student["middle_name"],
                    student["last_name"],
                    student["year_level"],
                    student["email"],
                    student["contact_number"],
                    student["course_code"],
                ),
            )

        # Set alternating row colors
        self.students_table.tag_configure("oddrow", background="#252525")
        self.students_table.tag_configure("evenrow", background="#353535")
        # Apply alternating colors to rows
        for index, student in enumerate(self.students_table.get_children()):
            if index % 2 == 0:
                self.students_table.item(student, tags=("evenrow",))
            else:
                self.students_table.item(student, tags=("oddrow",))

    def search(self):
        student_number = self.search_bar.get()

        if student_number == "":
            return

        db = Database()
        student = db.get_student(student_number)
        if student is not None:
            self.populate_students_table([student])
        else:
            messagebox.showwarning(
                "Student not found", "Student number not found in the database."
            )

    def reset_table(self):
        self.populate_students_table()
        self.search_bar.delete(0, "end")


class GradesTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")


class DocumentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")


class SMSTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")


# Example usage
login_screen = Login()
login_screen.mainloop()
