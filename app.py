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
            self.search_frame,
            text="🔍 Search", 
            command=self.get_selected_students, 
            width=40
        )
        self.reset_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            command=self.reset_table,
            fg_color="grey",
            width=20,
        )

        self.buttons_frame = ctk.CTkFrame(self)
        self.delete_student_button = ctk.CTkButton(
            self.buttons_frame,
            text="🗑 Delete Student",
            width=20,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_student_cmd,
        )
        self.edit_student_button = ctk.CTkButton(
            self.buttons_frame,
            text="Edit Student",
            width=20,
            command=self.edit_student_cmd,
        )
        self.add_student_button = ctk.CTkButton(
            self.buttons_frame,
            text="+ Add Student",
            width=20,
            command=self.add_student_cmd,
        )

        # Grid layout
        self.search_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        self.search_bar.grid(row=0, column=0, sticky="w")
        self.search_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.reset_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.delete_student_button.grid(row=0, column=0, sticky="e", padx=(10, 0))
        self.edit_student_button.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.add_student_button.grid(row=0, column=2, sticky="e", padx=(10, 0))
        self.students_table.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=2
        )

    def get_selected_students(self):
        selected = self.students_table.selection()
        if not selected:
            messagebox.showwarning(
                "No student selected", "Please select a student to delete."
            )
            return

        students = []
        for student in selected:
            students.append(self.students_table.item(student)["values"])

        return students

    def populate_students_table(self, students=None):
        if not students:
            db = Database()
            students = db.get_all("student_info")

        students = sorted(students, key=lambda student: student["student_id"])

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

    def delete_student_cmd(self):
        selected = self.get_selected_students()
        if not selected:
            messagebox.showwarning(
                "No student selected", "Please select a student to delete."
            )
            return

        confirmation = messagebox.askyesno(
            "Delete Student",
            "Are you sure you want to delete the selected student(s)?",
        )

        if confirmation:
            db = Database()
            for student in selected:
                db.delete_student(student[0])
            self.populate_students_table()

    def edit_student_cmd(self):
        selected = self.get_selected_students()
        if not selected:
            messagebox.showwarning(
                "No student selected", "Please select a student to edit."
            )
            return
        elif len(selected) > 1:
            messagebox.showwarning(
                "Too many students selected",
                "Please select only one student to edit.",
            )
            return

        db = Database()
        student_number = selected[0][0]
        student = db.get_student(student_number)
        edit_student_window = EditStudentWindow(self, student)
        edit_student_window.grab_set()

    def add_student_cmd(self):
        add_student_window = AddStudentWindow(self)
        add_student_window.grab_set()


class AddStudentWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Student")
        self.geometry("390x620")
        self.grid_columnconfigure(0, weight=1)

        self.student_number_label = ctk.CTkLabel(self, text="Student Number")
        self.student_number_entry = ctk.CTkEntry(self)

        self.first_name_label = ctk.CTkLabel(self, text="First Name")
        self.first_name_entry = ctk.CTkEntry(self)

        self.middle_name_label = ctk.CTkLabel(self, text="Middle Name")
        self.middle_name_entry = ctk.CTkEntry(self)

        self.last_name_label = ctk.CTkLabel(self, text="Last Name")
        self.last_name_entry = ctk.CTkEntry(self)

        self.year_level_label = ctk.CTkLabel(self, text="Year Level")
        self.year_level_entry = ctk.CTkEntry(self)

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_entry = ctk.CTkEntry(self)

        self.contact_number_label = ctk.CTkLabel(self, text="Contact Number")
        self.contact_number_entry = ctk.CTkEntry(self)

        self.course_code_label = ctk.CTkLabel(self, text="Course Code")
        self.course_code_entry = ctk.CTkEntry(self)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        self.student_number_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_number_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.first_name_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.first_name_entry.grid(row=3, column=0, padx=10, sticky="ew")

        self.middle_name_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.middle_name_entry.grid(row=5, column=0, padx=10, sticky="ew")

        self.last_name_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.last_name_entry.grid(row=7, column=0, padx=10, sticky="ew")

        self.year_level_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.year_level_entry.grid(row=9, column=0, padx=10, sticky="ew")

        self.email_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="w")
        self.email_entry.grid(row=11, column=0, padx=10, sticky="ew")

        self.contact_number_label.grid(
            row=12, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.contact_number_entry.grid(row=13, column=0, padx=10, sticky="ew")

        self.course_code_label.grid(row=14, column=0, padx=10, pady=(10, 0), sticky="w")
        self.course_code_entry.grid(row=15, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=16, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        student_number = self.student_number_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        year_level = self.year_level_entry.get()
        email = self.email_entry.get()
        contact_number = self.contact_number_entry.get()
        course_code = self.course_code_entry.get()

        # Validate the data
        if not (
            student_number
            and first_name
            and last_name
            and year_level
            and email
            and contact_number
            and course_code
        ):
            messagebox.showwarning(
                "Missing Fields", "Please fill out all fields before submitting."
            )
            return

        if not student_number.isdigit() and len(student_number) != 9:
            messagebox.showwarning(
                "Invalid Student Number",
                "Please enter a valid student number.",
            )
            return

        if not year_level.isdigit() and len(year_level) > 5 and len(year_level) < 1:
            messagebox.showwarning(
                "Invalid Year Level",
                "Please enter a valid year level.",
            )
            return

        if not contact_number.isdigit() and len(contact_number) != 11:
            messagebox.showwarning(
                "Invalid Contact Number",
                "Please enter a valid contact number.",
            )
            return

        db = Database()
        if db.get_student(student_number) is not None:
            messagebox.showwarning(
                "Student already exists",
                "Student number already exists in the database.",
            )
            return

        db.insert_student(
            {
                "student_id": student_number,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "year_level": year_level,
                "email": email,
                "contact_number": contact_number,
                "course_code": course_code,
            }
        )
        self.master.populate_students_table()
        self.destroy()


class EditStudentWindow(ctk.CTkToplevel):
    def __init__(self, master, student):
        super().__init__(master)
        self.title("Edit Student")
        self.geometry("390x620")
        self.grid_columnconfigure(0, weight=1)

        self.student_number_label = ctk.CTkLabel(self, text="Student Number")
        self.student_number_entry = ctk.CTkEntry(self)
        self.student_number_entry.insert(0, student["student_id"])
        self.student_number_entry.configure(state="disabled")

        self.first_name_label = ctk.CTkLabel(self, text="First Name")
        self.first_name_entry = ctk.CTkEntry(self)
        self.first_name_entry.insert(0, student["first_name"])

        self.middle_name_label = ctk.CTkLabel(self, text="Middle Name")
        self.middle_name_entry = ctk.CTkEntry(self)
        self.middle_name_entry.insert(0, student["middle_name"])

        self.last_name_label = ctk.CTkLabel(self, text="Last Name")
        self.last_name_entry = ctk.CTkEntry(self)
        self.last_name_entry.insert(0, student["last_name"])

        self.year_level_label = ctk.CTkLabel(self, text="Year Level")
        self.year_level_entry = ctk.CTkEntry(self)
        self.year_level_entry.insert(0, student["year_level"])

        self.email_label = ctk.CTkLabel(self, text="Email")
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.insert(0, student["email"])

        self.contact_number_label = ctk.CTkLabel(self, text="Contact Number")
        self.contact_number_entry = ctk.CTkEntry(self)
        self.contact_number_entry.insert(0, student["contact_number"])

        self.course_code_label = ctk.CTkLabel(self, text="Course Code")
        self.course_code_entry = ctk.CTkEntry(self)
        self.course_code_entry.insert(0, student["course_code"])

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        self.student_number_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_number_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.first_name_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.first_name_entry.grid(row=3, column=0, padx=10, sticky="ew")

        self.middle_name_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.middle_name_entry.grid(row=5, column=0, padx=10, sticky="ew")

        self.last_name_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.last_name_entry.grid(row=7, column=0, padx=10, sticky="ew")

        self.year_level_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.year_level_entry.grid(row=9, column=0, padx=10, sticky="ew")

        self.email_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="w")
        self.email_entry.grid(row=11, column=0, padx=10, sticky="ew")

        self.contact_number_label.grid(
            row=12, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.contact_number_entry.grid(row=13, column=0, padx=10, sticky="ew")

        self.course_code_label.grid(row=14, column=0, padx=10, pady=(10, 0), sticky="w")
        self.course_code_entry.grid(row=15, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=16, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        student_number = self.student_number_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        year_level = self.year_level_entry.get()
        email = self.email_entry.get()
        contact_number = self.contact_number_entry.get()
        course_code = self.course_code_entry.get()

        # Validate the data
        if not (
            student_number
            and first_name
            and last_name
            and year_level
            and email
            and contact_number
            and course_code
        ):
            messagebox.showwarning(
                "Missing Fields", "Please fill out all fields before submitting."
            )
            return

        if not student_number.isdigit() and len(student_number) != 9:
            messagebox.showwarning(
                "Invalid Student Number",
                "Please enter a valid student number.",
            )
            return

        if not year_level.isdigit() and len(year_level) > 5 and len(year_level) < 1:
            messagebox.showwarning(
                "Invalid Year Level",
                "Please enter a valid year level.",
            )
            return

        if not contact_number.isdigit() and len(contact_number) != 11:
            messagebox.showwarning(
                "Invalid Contact Number",
                "Please enter a valid contact number.",
            )
            return

        db = Database()
        db.update_student(
            student_number,
            {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "year_level": year_level,
                "email": email,
                "contact_number": contact_number,
                "course_code": course_code,
            },
        )
        self.master.populate_students_table()
        self.destroy()


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
