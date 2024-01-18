import select
import tkinter.messagebox as messagebox
from utils.database import Database
import customtkinter as ctk
from tkinter import ttk
from datetime import datetime

ctk.set_appearance_mode("dark")


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
        self.title("Office of the University Registrar Inquiry System")
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

        self.buttons_frame = ctk.CTkFrame(self)
        self.import_excel_button = ctk.CTkButton(
            self.buttons_frame,
            text="📄 Import from Excel",
            command=self.import_excel_cmd,
            width=20,
            fg_color="green",
            hover_color="darkgreen",
        )
        self.delete_student_button = ctk.CTkButton(
            self.buttons_frame,
            text="🗑",
            width=20,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_student_cmd,
        )
        self.edit_student_button = ctk.CTkButton(
            self.buttons_frame,
            text="🖋",
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
        self.import_excel_button.grid(row=0, column=0, sticky="e", padx=(10, 0))
        self.delete_student_button.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.edit_student_button.grid(row=0, column=2, sticky="e", padx=(10, 0))
        self.add_student_button.grid(row=0, column=3, sticky="e", padx=(10, 0))
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

    def import_excel_cmd(self):
        # open file dialog
        from tkinter import filedialog
        import pandas as pd

        # Only allow excel files
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        if file_path == "":
            return

        # Read the excel file
        df = pd.read_excel(file_path)

        # Validate the data
        if not (
            "student_id" in df.columns
            and "first_name" in df.columns
            and "last_name" in df.columns
            and "year_level" in df.columns
            and "email" in df.columns
            and "contact_number" in df.columns
            and "course_code" in df.columns
        ):
            messagebox.showwarning(
                "Invalid Excel File",
                "The excel file you selected is invalid.",
            )
            return

        # Convert the dataframe to a list of dictionaries
        students = df.to_dict("records")

        # Insert the students into the database
        db = Database()
        skipped = 0
        for student in students:
            # Check if the student already exists
            if db.get_student(student["student_id"]) is not None:
                skipped += 1
                continue

            db.insert_student(student)

        self.populate_students_table()

        # Show a message box with the number of students imported
        if skipped > 0:
            messagebox.showinfo(
                "Import Successful",
                f"{len(students) - skipped} student(s) imported. {skipped} student(s) skipped because they already exist.",
            )
        else:
            messagebox.showinfo(
                "Import Successful",
                f"{len(students)} student(s) imported.",
            )


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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Variables
        self.student = None
        self.grades = None
        self.year = None
        self.semester = None

        # Widgets
        self.preview_frame = ctk.CTkFrame(self, corner_radius=0)
        self.labels_frame = ctk.CTkFrame(self.preview_frame, corner_radius=0)
        self.values_frame = ctk.CTkFrame(self.preview_frame, corner_radius=0)
        self.student_number_label = ctk.CTkLabel(
            self.labels_frame, text="Student Number"
        )
        self.student_number_value = ctk.CTkLabel(self.values_frame, text="")
        self.student_name_label = ctk.CTkLabel(self.labels_frame, text="Student Name")
        self.student_name_value = ctk.CTkLabel(self.values_frame, text="")
        self.course_label = ctk.CTkLabel(self.labels_frame, text="Course")
        self.course_value = ctk.CTkLabel(self.values_frame, text="")
        self.year_level_label = ctk.CTkLabel(self.labels_frame, text="Year Level")
        self.year_level_value = ctk.CTkLabel(self.values_frame, text="")

        self.labels_frame.configure(fg_color="#252525")
        self.values_frame.configure(fg_color="#353535")

        self.search_frame = ctk.CTkFrame(self)
        self.search_bar = ctk.CTkEntry(
            self.search_frame, placeholder_text="Enter student no."
        )
        self.year_option_label = ctk.StringVar(value="Year")
        self.year_option = ctk.CTkOptionMenu(
            self.search_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.year_option_label,
            command=self.year_option_callback,
        )
        self.semester_option_label = ctk.StringVar(value="Semester")
        self.semester_option = ctk.CTkOptionMenu(
            self.search_frame,
            values=["1", "2"],
            variable=self.semester_option_label,
            command=self.semester_option_callback,
        )
        self.search_button = ctk.CTkButton(
            self.search_frame, text="🔍 Search", command=self.search, width=40
        )
        self.reset_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            command=self.reset,
            fg_color="grey",
            width=20,
        )

        self.buttons_frame = ctk.CTkFrame(self)
        self.delete_grade_button = ctk.CTkButton(
            self.buttons_frame,
            text="🗑",
            width=20,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_grade_cmd,
        )
        self.edit_grade_button = ctk.CTkButton(
            self.buttons_frame,
            text="🖋",
            width=20,
            command=self.edit_grade_cmd,
        )
        self.add_grade_button = ctk.CTkButton(
            self.buttons_frame,
            text="+ Add Grade",
            width=20,
            command=self.add_grade_cmd,
        )

        self.grades_table = ttk.Treeview(
            self,
            columns=(
                "subject_code",
                "subject_title",
                "units",
                "grade",
                "remarks",
            ),
            show="headings",
        )
        self.grades_table.heading("subject_code", text="Subject Code")
        self.grades_table.heading("subject_title", text="Subject Title")
        self.grades_table.heading("units", text="Units")
        self.grades_table.heading("grade", text="Grade")
        self.grades_table.heading("remarks", text="Remarks")

        # Grid layout
        self.preview_frame.grid(
            row=0, column=0, sticky="ew", padx=10, pady=(10, 0), columnspan=2
        )
        self.preview_frame.grid_columnconfigure(0, weight=0)
        self.preview_frame.grid_columnconfigure(1, weight=2)
        self.labels_frame.grid(row=0, column=0, sticky="ew")
        self.values_frame.grid(row=0, column=1, sticky="ew")
        self.student_number_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_number_value.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_name_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.student_name_value.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.course_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.course_value.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.year_level_label.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")
        self.year_level_value.grid(row=3, column=0, padx=10, pady=(10, 10), sticky="w")
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=20)
        self.buttons_frame.grid(row=1, column=1, sticky="e", padx=10, pady=20)
        self.search_bar.grid(row=0, column=0, sticky="w")
        self.year_option.grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.semester_option.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.search_button.grid(row=0, column=3, sticky="w", padx=(10, 0))
        self.reset_button.grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.delete_grade_button.grid(row=0, column=0, sticky="e", padx=(10, 0))
        self.edit_grade_button.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.add_grade_button.grid(row=0, column=2, sticky="e", padx=(10, 0))
        self.grades_table.grid(
            row=2, column=0, sticky="nsew", padx=10, pady=(0, 10), columnspan=2
        )

    def set_preview(self, student_number, student_name, course, year_level):
        self.student_number_value.configure(text=student_number)
        self.student_name_value.configure(text=student_name)
        self.course_value.configure(text=course)
        self.year_level_value.configure(text=year_level)

    def search(self):
        student_number = self.search_bar.get()

        if student_number == "":
            return

        if self.year is None or self.semester is None:
            messagebox.showwarning(
                "Missing Year and Semester", "Please select a year and semester."
            )
            return

        db = Database()
        student_grade = db.get_student_grade(student_number, self.year, self.semester)
        student_info = db.get_student(student_number)

        if student_info is None:
            messagebox.showwarning(
                "Student not found", "Student number not found in the database."
            )
            return

        self.student = student_info
        self.grades = student_grade
        self.set_preview(
            student_info["student_id"],
            f"{student_info['first_name']} {student_info['middle_name']} {student_info['last_name']}",
            student_info["course_code"],
            student_info["year_level"],
        )
        self.populate_grades_table(student_grade)

    def reset(self):
        self.set_preview("", "", "", "")
        self.populate_grades_table()
        self.year_option_label.set("Year")
        self.semester_option_label.set("Semester")
        self.student = None
        self.grades = None
        self.year = None
        self.semester = None

    def populate_grades_table(self, grades=None):
        self.grades_table.delete(*self.grades_table.get_children())

        if grades is None:
            return

        for grade in grades:
            self.grades_table.insert(
                "",
                "end",
                values=(
                    grade["subjects"]["code"],
                    grade["subjects"]["title"],
                    grade["subjects"]["units"],
                    "-" if grade["grade"] is None else "{:.2f}".format(grade["grade"]),
                    grade["remarks"]["remark"],
                ),
            )

        # Set alternating row colors
        self.grades_table.tag_configure("oddrow", background="#252525")
        self.grades_table.tag_configure("evenrow", background="#353535")
        # Apply alternating colors to rows
        for index, grade in enumerate(self.grades_table.get_children()):
            if index % 2 == 0:
                self.grades_table.item(grade, tags=("evenrow",))
            else:
                self.grades_table.item(grade, tags=("oddrow",))

    def delete_grade_cmd(self):
        selected = self.grades_table.selection()
        if not selected:
            messagebox.showwarning(
                "No grade selected", "Please select a grade to delete."
            )
            return

        confirmation = messagebox.askyesno(
            "Delete Grade",
            "Are you sure you want to delete the selected grade(s)?",
        )

        if confirmation:
            # Get the index of the selected grades
            indexes = []
            for grade in selected:
                indexes.append(self.grades_table.index(grade))

            # Delete the grades from the database
            db = Database()
            for index in indexes:
                db.delete_grade(self.grades[index]["grade_id"])

            self.grades = db.get_student_grade(
                self.student["student_id"], self.year, self.semester
            )
            self.populate_grades_table(self.grades)

    def edit_grade_cmd(self):
        selected = self.grades_table.selection()
        if not selected:
            messagebox.showwarning(
                "No grade selected", "Please select a grade to edit."
            )
            return
        elif len(selected) > 1:
            messagebox.showwarning(
                "Too many grades selected",
                "Please select only one grade to edit.",
            )
            return

        # Get the index of the selected grade
        index = self.grades_table.index(selected[0])

        edit_grade_window = EditGradeWindow(self, self.grades[index])
        edit_grade_window.grab_set()

    def add_grade_cmd(self):
        # Check if a student is selected and a year and sem
        if self.student is None:
            messagebox.showwarning("No student selected", "Please select a student.")
            return

        if self.year is None or self.semester is None:
            messagebox.showwarning(
                "Missing Year and Semester", "Please select a year and semester."
            )
            return

        add_grade_window = AddGradeWindow(self, self.student, self.year, self.semester)
        add_grade_window.grab_set()

    def year_option_callback(self, value):
        self.year = value

    def semester_option_callback(self, value):
        self.semester = value


class AddGradeWindow(ctk.CTkToplevel):
    def __init__(self, master, student, year, semester):
        super().__init__(master)
        self.title("Add Grade")
        self.grid_columnconfigure(0, weight=1)

        self.student = student
        self.year = year
        self.semester = semester

        self.subject_code_label = ctk.CTkLabel(self, text="Subject Code")
        self.subject_code_entry = ctk.CTkEntry(self)

        self.grade_label = ctk.CTkLabel(self, text="Grade")
        self.grade_entry = ctk.CTkEntry(self)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        self.subject_code_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.subject_code_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.grade_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.grade_entry.grid(row=3, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=4, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        subject_code = self.subject_code_entry.get()
        grade = self.grade_entry.get()

        # Validate the data
        if not subject_code:
            messagebox.showwarning(
                "Missing Fields", "Please fill out necessary fields before submitting."
            )
            return

        if not validate_grade(grade):
            messagebox.showwarning(
                "Invalid Grade",
                "Please enter a valid grade (1-5).",
            )
            return

        grade = None if grade == "" else float(grade)

        db = Database()
        db.insert_grade(
            {
                "student_id": self.student["student_id"],
                "year": self.year,
                "sem": self.semester,
                "subject_code": subject_code,
                "grade": grade,
                "remark_id": infer_remark(grade),
            }
        )
        self.master.grades = db.get_student_grade(
            self.student["student_id"], self.year, self.semester
        )
        self.master.populate_grades_table(self.master.grades)
        self.destroy()


def infer_remark(grade):
    if grade is None:
        return 3
    elif grade <= 3:
        return 1
    elif grade > 3:
        return 2


def validate_grade(grade):
    try:
        grade = None if grade == "" else float(grade)
    except ValueError:
        return False

    if grade and not (1 <= grade <= 5):
        return False

    return True


class EditGradeWindow(ctk.CTkToplevel):
    def __init__(self, master, grade):
        super().__init__(master)
        self.title("Edit Grade")
        self.grid_columnconfigure(0, weight=1)

        self.grade = grade

        self.subject_code_label = ctk.CTkLabel(self, text="Subject Code")
        self.subject_code_entry = ctk.CTkEntry(self)
        self.subject_code_entry.insert(0, grade["subjects"]["code"])
        self.subject_code_entry.configure(state="disabled")

        self.grade_label = ctk.CTkLabel(self, text="Grade")
        self.grade_entry = ctk.CTkEntry(self)
        self.grade_entry.insert(0, "" if grade["grade"] is None else grade["grade"])

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        self.subject_code_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.subject_code_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.grade_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.grade_entry.grid(row=3, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=4, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        grade = self.grade_entry.get()

        if not validate_grade(grade):
            messagebox.showwarning(
                "Invalid Grade",
                "Please enter a valid grade (1-5).",
            )
            return

        grade = None if grade == "" else float(grade)

        db = Database()
        db.update_grade(
            self.grade["grade_id"],
            {
                "grade": grade,
                "remark_id": infer_remark(grade),
            },
        )
        self.master.grades = db.get_student_grade(
            self.grade["student_id"], self.grade["year"], self.grade["sem"]
        )
        self.master.populate_grades_table(self.master.grades)
        self.destroy()


class DocumentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Widgets
        self.documents_table = ttk.Treeview(
            self,
            columns=(
                "request_id",
                "student_id",
                "mode",
                "document_type",
                "num_of_copies",
                "purpose",
                "paid_amount",
                "receipt_no",
                "payment_date",
                "requested_date",
                "received_date",
                "status",
            ),
            show="headings",
            selectmode="extended",
        )
        # Header setup
        self.documents_table.heading("request_id", text="Request ID")
        self.documents_table.heading("student_id", text="Student ID")
        self.documents_table.heading("mode", text="Mode")
        self.documents_table.heading("document_type", text="Document Type")
        self.documents_table.heading("num_of_copies", text="Number of Copies")
        self.documents_table.heading("purpose", text="Purpose")
        self.documents_table.heading("paid_amount", text="Paid Amount")
        self.documents_table.heading("receipt_no", text="Receipt No.")
        self.documents_table.heading("payment_date", text="Payment Date")
        self.documents_table.heading("requested_date", text="Requested Date")
        self.documents_table.heading("received_date", text="Received Date")
        self.documents_table.heading("status", text="Status")

        self.populate_documents_table()

        s = ttk.Style()
        s.configure("Treeview", rowheight=25)

        self.search_frame = ctk.CTkFrame(self)
        self.search_bar = ctk.CTkEntry(
            self.search_frame, placeholder_text="Enter request ID"
        )
        self.search_button = ctk.CTkButton(
            self.search_frame, text="🔍 Search", command=self.search, width=40
        )
        self.reset_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            command=self.reset,
            fg_color="grey",
            width=20,
        )

        self.status_filter_options = ["Pending", "Ready", "Claimed"]
        self.status_filter = ctk.CTkOptionMenu(
            self.search_frame,
            values=self.status_filter_options,
            command=self.status_filter_callback,
        )
        self.status_filter.set(self.status_filter_options[0])

        self.buttons_frame = ctk.CTkFrame(self)
        self.mark_as_claimed_button = ctk.CTkButton(
            self.buttons_frame,
            text="Mark as Claimed",
            command=self.mark_as_claimed_cmd,
            width=20,
            fg_color="grey",
            hover_color="darkgrey",
        )
        self.mark_as_ready_button = ctk.CTkButton(
            self.buttons_frame,
            text="Mark as Ready",
            command=self.mark_as_ready_cmd,
            width=20,
            fg_color="grey",
            hover_color="darkgrey",
        )
        self.delete_document_button = ctk.CTkButton(
            self.buttons_frame,
            text="🗑",
            width=20,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_document_cmd,
        )
        self.edit_document_button = ctk.CTkButton(
            self.buttons_frame,
            text="🖋",
            width=20,
            command=self.edit_document_cmd,
        )
        self.add_document_button = ctk.CTkButton(
            self.buttons_frame,
            text="+ Add Document",
            width=20,
            command=self.add_document_cmd,
        )

        # Grid layout
        self.search_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.buttons_frame.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        self.search_bar.grid(row=0, column=0, sticky="w")
        self.search_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        self.reset_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.status_filter.grid(row=0, column=3, sticky="w", padx=(10, 0))
        self.mark_as_claimed_button.grid(row=0, column=0, sticky="e", padx=(10, 0))
        self.mark_as_ready_button.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.delete_document_button.grid(row=0, column=2, sticky="e", padx=(10, 0))
        self.edit_document_button.grid(row=0, column=3, sticky="e", padx=(10, 0))
        self.add_document_button.grid(row=0, column=4, sticky="e", padx=(10, 0))
        self.documents_table.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=2
        )

    def populate_documents_table(self, documents=None):
        self.documents_table.delete(*self.documents_table.get_children())

        if documents is None:
            db = Database()
            documents = db.get_document_requests_by_status("pending")
        
        self.documents = documents

        for document in documents:
            self.documents_table.insert(
                "",
                "end",
                values=(
                    document["id"],
                    document["student_id"],
                    document["mode"],
                    document["document_type"]["type"],
                    document["request_amount"],
                    document["purpose"],
                    document["total"],
                    document["receipt_no"],
                    document["payment_date"],
                    document["request_date"],
                    document["receive_date"],
                    document["request_statuses"]["status"],
                ),
            )

        # Set alternating row colors
        self.documents_table.tag_configure("oddrow", background="#252525")
        self.documents_table.tag_configure("evenrow", background="#353535")
        # Apply alternating colors to rows
        for index, document in enumerate(self.documents_table.get_children()):
            if index % 2 == 0:
                self.documents_table.item(document, tags=("evenrow",))
            else:
                self.documents_table.item(document, tags=("oddrow",))

    def search(self):
        request_id = self.search_bar.get()

        if request_id == "":
            return

        db = Database()
        document = db.get_document_request(request_id)

        if document is None:
            messagebox.showwarning(
                "Record not found", "Request ID not found in the database."
            )
            return

        self.populate_documents_table([document])

    def reset(self):
        self.populate_documents_table()
        self.search_bar.delete(0, "end")
        self.documents = None

    def status_filter_callback(self, value):
        db = Database()
        documents = db.get_document_requests_by_status(value.lower())
        self.populate_documents_table(documents)

    def mark_as_claimed_cmd(self):
        # Implement the logic to mark selected documents as claimed
        pass

    def mark_as_ready_cmd(self):
        # Implement the logic to mark selected documents as ready
        pass

    def delete_document_cmd(self):
        # Implement the logic to delete selected documents
        pass

    def edit_document_cmd(self):
        # Edit a document request
        selected = self.documents_table.selection()
        if not selected:
            messagebox.showwarning(
                "No record selected", "Please select a record to edit."
            )
            return
        
        if len(selected) > 1:
            messagebox.showwarning(
                "Too many records selected",
                "Please select only one record to edit.",
            )
            return
        
        # Get the index of the selected record
        index = self.documents_table.index(selected[0])

        edit_document_window = EditDocumentWindow(self, self.documents[index])
        edit_document_window.grab_set()

    def add_document_cmd(self):
        # Add a document request
        add_request_window = AddRequestWindow(self)
        add_request_window.grab_set()


class AddRequestWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Document Request")
        self.grid_columnconfigure(0, weight=1)

        self.student_number_label = ctk.CTkLabel(self, text="Student Number")
        self.student_number_entry = ctk.CTkEntry(self)

        self.mode_label = ctk.CTkLabel(self, text="Mode")
        self.mode_option_label = ctk.StringVar(value="Walk-in")
        self.mode_option = ctk.CTkOptionMenu(
            self,
            values=["Walk-in", "Online"],
            variable=self.mode_option_label,
        )

        db = Database()
        self.document_types = db.get_document_types()
        self.document_type_options = {}
        
        # Map document type to type id
        for document_type in self.document_types:
            self.document_type_options[document_type["type"]] = document_type["id"]

        document_type_option_list = list(self.document_type_options.keys())

        self.document_type_label = ctk.CTkLabel(self, text="Document Type")
        self.document_type_option = ctk.CTkOptionMenu(
            self,
            values=document_type_option_list,
        )

        # set default value
        self.document_type_option.set(document_type_option_list[0])

        self.num_of_copies_label = ctk.CTkLabel(self, text="Number of Copies")
        self.num_of_copies_entry = ctk.CTkEntry(self)

        self.purpose_label = ctk.CTkLabel(self, text="Purpose")
        self.purpose_entry = ctk.CTkEntry(self)

        self.amount_paid_label = ctk.CTkLabel(self, text="Amount Paid")
        self.amount_paid_entry = ctk.CTkEntry(self)

        self.receipt_no_label = ctk.CTkLabel(self, text="Receipt No.")
        self.receipt_no_entry = ctk.CTkEntry(self)

        self.payment_date_label = ctk.CTkLabel(self, text="Payment Date")
        self.payment_date_entry = ctk.CTkEntry(self)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        # Grid
        self.student_number_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_number_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.mode_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.mode_option.grid(row=3, column=0, padx=10, sticky="ew")

        self.document_type_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.document_type_option.grid(row=5, column=0, padx=10, sticky="ew")

        self.num_of_copies_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.num_of_copies_entry.grid(row=7, column=0, padx=10, sticky="ew")

        self.purpose_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.purpose_entry.grid(row=9, column=0, padx=10, sticky="ew")

        self.amount_paid_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="w")
        self.amount_paid_entry.grid(row=11, column=0, padx=10, sticky="ew")

        self.receipt_no_label.grid(row=12, column=0, padx=10, pady=(10, 0), sticky="w")
        self.receipt_no_entry.grid(row=13, column=0, padx=10, sticky="ew")

        self.payment_date_label.grid(row=14, column=0, padx=10, pady=(10, 0), sticky="w")
        self.payment_date_entry.grid(row=15, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=16, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        student_number = self.student_number_entry.get()
        mode = self.mode_option_label.get()
        document_type = self.document_type_option.get()
        num_of_copies = self.num_of_copies_entry.get()
        purpose = self.purpose_entry.get()
        amount_paid = self.amount_paid_entry.get()
        receipt_no = self.receipt_no_entry.get()
        payment_date = self.payment_date_entry.get()

        # Validate the data
        if not (
            student_number
            and mode
            and document_type
            and num_of_copies
            and purpose
            and amount_paid
            and receipt_no
            and payment_date
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
        
        db = Database()
        temp_student = db.get_student(student_number)
        student_exists = temp_student is not None

        if not student_exists:
            messagebox.showwarning(
                "Student not found",
                "Student number not found in the database.",
            )
            return

        if not num_of_copies.isdigit():
            messagebox.showwarning(
                "Invalid Number of Copies",
                "Please enter a valid number of copies.",
            )
            return

        if not amount_paid.isdigit():
            messagebox.showwarning(
                "Invalid Amount Paid",
                "Please enter a valid amount paid.",
            )
            return

        if not receipt_no.isdigit():
            messagebox.showwarning(
                "Invalid Receipt Number",
                "Please enter a valid receipt number.",
            )
            return
    
        # Check payment date format (yyyy-mm-dd)
        try:
            datetime.strptime(payment_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Invalid Payment Date",
                "Please enter a valid payment date (yyyy-mm-dd).",
            )
            return

        db = Database()
        if db.get_student(student_number) is None:
            messagebox.showwarning(
                "Student not found",
                "Student number not found in the database.",
            )
            return

        db.insert_document_request(
            {
                "student_id": student_number,
                "mode": mode,
                "document_type_id": self.document_type_options[document_type],
                "request_amount": num_of_copies,
                "purpose": purpose,
                "total": amount_paid,
                "receipt_no": receipt_no,
                "payment_date": payment_date,
                "request_date": datetime.now().strftime("%Y-%m-%d"),
                "receive_date": None,
            }
        )
        self.master.populate_documents_table()
        self.destroy()


class EditDocumentWindow(ctk.CTkToplevel):
    def __init__(self, master, document):
        super().__init__(master)
        self.title("Edit Document Request")
        self.grid_columnconfigure(0, weight=1)

        self.document = document

        self.student_number_label = ctk.CTkLabel(self, text="Student Number")
        self.student_number_entry = ctk.CTkEntry(self)
        self.student_number_entry.insert(0, document["student_id"])

        self.mode_label = ctk.CTkLabel(self, text="Mode")
        self.mode_option_label = ctk.StringVar(value=document["mode"])
        self.mode_option = ctk.CTkOptionMenu(
            self,
            values=["Walk-in", "Online"],
            variable=self.mode_option_label,
        )

        db = Database()
        self.document_types = db.get_document_types()
        self.document_type_options = {}
        
        # Map document type to type id
        for document_type in self.document_types:
            self.document_type_options[document_type["type"]] = document_type["id"]

        document_type_option_list = list(self.document_type_options.keys())

        self.document_type_label = ctk.CTkLabel(self, text="Document Type")
        self.document_type_option = ctk.CTkOptionMenu(
            self,
            values=document_type_option_list,
        )

        # set default value
        self.document_type_option.set(document_type_option_list[0])

        self.num_of_copies_label = ctk.CTkLabel(self, text="Number of Copies")
        self.num_of_copies_entry = ctk.CTkEntry(self)
        self.num_of_copies_entry.insert(0, document["request_amount"])

        self.purpose_label = ctk.CTkLabel(self, text="Purpose")
        self.purpose_entry = ctk.CTkEntry(self)
        self.purpose_entry.insert(0, document["purpose"])

        self.amount_paid_label = ctk.CTkLabel(self, text="Amount Paid")
        self.amount_paid_entry = ctk.CTkEntry(self)
        self.amount_paid_entry.insert(0, document["total"])

        self.receipt_no_label = ctk.CTkLabel(self, text="Receipt No.")
        self.receipt_no_entry = ctk.CTkEntry(self)
        self.receipt_no_entry.insert(0, document["receipt_no"])

        self.payment_date_label = ctk.CTkLabel(self, text="Payment Date")
        self.payment_date_entry = ctk.CTkEntry(self)
        self.payment_date_entry.insert(0, document["payment_date"])

        self.request_date_label = ctk.CTkLabel(self, text="Request Date")
        self.request_date_entry = ctk.CTkEntry(self)
        self.request_date_entry.insert(0, document["request_date"])

        self.receive_date_label = ctk.CTkLabel(self, text="Receive Date")
        self.receive_date_entry = ctk.CTkEntry(self)
        if document["receive_date"] is not None:
            self.receive_date_entry.insert(0, document["receive_date"])

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit)

        # Grid
        self.student_number_label.grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w"
        )
        self.student_number_entry.grid(row=1, column=0, padx=10, sticky="ew")

        self.mode_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.mode_option.grid(row=3, column=0, padx=10, sticky="ew")

        self.document_type_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")
        self.document_type_option.grid(row=5, column=0, padx=10, sticky="ew")

        self.num_of_copies_label.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")
        self.num_of_copies_entry.grid(row=7, column=0, padx=10, sticky="ew")

        self.purpose_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.purpose_entry.grid(row=9, column=0, padx=10, sticky="ew")

        self.amount_paid_label.grid(row=10, column=0, padx=10, pady=(10, 0), sticky="w")
        self.amount_paid_entry.grid(row=11, column=0, padx=10, sticky="ew")

        self.receipt_no_label.grid(row=12, column=0, padx=10, pady=(10, 0), sticky="w")
        self.receipt_no_entry.grid(row=13, column=0, padx=10, sticky="ew")

        self.payment_date_label.grid(row=14, column=0, padx=10, pady=(10, 0), sticky="w")
        self.payment_date_entry.grid(row=15, column=0, padx=10, sticky="ew")

        self.request_date_label.grid(row=16, column=0, padx=10, pady=(10, 0), sticky="w")
        self.request_date_entry.grid(row=17, column=0, padx=10, sticky="ew")

        self.receive_date_label.grid(row=18, column=0, padx=10, pady=(10, 0), sticky="w")
        self.receive_date_entry.grid(row=19, column=0, padx=10, sticky="ew")

        self.submit_button.grid(row=20, column=0, padx=10, pady=(20, 10), sticky="ew")

    def submit(self):
        student_number = self.student_number_entry.get()
        mode = self.mode_option_label.get()
        document_type = self.document_type_option.get()
        num_of_copies = self.num_of_copies_entry.get()
        purpose = self.purpose_entry.get()
        amount_paid = self.amount_paid_entry.get()
        receipt_no = self.receipt_no_entry.get()
        payment_date = self.payment_date_entry.get()
        request_date = self.request_date_entry.get()
        receive_date = self.receive_date_entry.get()

        # Validate the data
        if not (
            student_number
            and mode
            and document_type
            and num_of_copies
            and purpose
            and amount_paid
            and receipt_no
            and payment_date
            and request_date
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
        
        db = Database()
        temp_student = db.get_student(student_number)
        student_exists = temp_student is not None

        if not student_exists:
            messagebox.showwarning(
                "Student not found",
                "Student number not found in the database.",
            )
            return

        if not num_of_copies.isdigit():
            messagebox.showwarning(
                "Invalid Number of Copies",
                "Please enter a valid number of copies.",
            )
            return

        if not amount_paid.isdigit():
            messagebox.showwarning(
                "Invalid Amount Paid",
                "Please enter a valid amount paid.",
            )
            return

        if not receipt_no.isdigit():
            messagebox.showwarning(
                "Invalid Receipt Number",
                "Please enter a valid receipt number.",
            )
            return
    
        # Check payment date format (yyyy-mm-dd)
        try:
            datetime.strptime(payment_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Invalid Payment Date",
                "Please enter a valid payment date (yyyy-mm-dd).",
            )
            return

        # Check request date format (yyyy-mm-dd)
        try:
            datetime.strptime(request_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning(
                "Invalid Request Date",
                "Please enter a valid request date (yyyy-mm-dd).",
            )
            return
        
        # Check receive date format (yyyy-mm-dd)
        if receive_date != "":
            try:
                datetime.strptime(receive_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Invalid Receive Date",
                    "Please enter a valid receive date (yyyy-mm-dd).",
                )
                return

        db = Database()
        db.update_document_request(
            self.document["id"],
            {
                "student_id": student_number,
                "mode": mode,
                "document_type_id": self.document_type_options[document_type],
                "request_amount": num_of_copies,
                "purpose": purpose,
                "total": amount_paid,
                "receipt_no": receipt_no,
                "payment_date": payment_date,
                "request_date": request_date,
                "receive_date": receive_date if receive_date != "" else None,
            },
        )

        self.master.populate_documents_table()
        self.destroy()

class SMSTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")


# Example usage
login_screen = Login()
login_screen.mainloop()
