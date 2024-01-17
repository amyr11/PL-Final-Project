import tkinter.messagebox as messagebox
from utils.database import Database
import customtkinter as ctk


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
            self.destroy()  # Close the login window
            main_window = MainWindow()
            main_window.mainloop()
        else:
            messagebox.showerror(
                "Invalid Credentials", "Invalid employee number or password."
            )


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
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


class StudentsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")


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
login_screen = MainWindow()
login_screen.mainloop()
