import tkinter.messagebox as messagebox
from utils.database import Database
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, CTkFrame


class Login(CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.grid_columnconfigure(0, weight=1)

        # Form widgets
        self.title_frame = CTkFrame(self)
        self.title_label = CTkLabel(
            self.title_frame, text="Office of the University Registrar", font=("", 24)
        )
        self.title_label.pack(padx=40, pady=(10, 0))
        self.subtitle_label = CTkLabel(
            self.title_frame, text="Inquiry System", font=("", 16)
        )
        self.subtitle_label.pack(padx=20, pady=(0, 20))

        self.employee_number_label = CTkLabel(self, text="Employee Number")
        self.employee_number_entry = CTkEntry(self)

        self.password_label = CTkLabel(self, text="Password")
        self.password_entry = CTkEntry(self, show="*")

        self.login_button = CTkButton(self, text="Login", command=self.login)

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
            main_window = MainWindow(employee_number)
            main_window.mainloop()
        else:
            messagebox.showerror(
                "Invalid Credentials", "Invalid employee number or password."
            )


class MainWindow(CTk):
    def __init__(self, employee_number):
        super().__init__()
        self.title("Main Window")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)

        # Add your main window content here
        welcome_label = CTkLabel(self, text=f"Welcome, Employee {employee_number}!")
        welcome_label.pack(padx=20, pady=20)


# Example usage
login_screen = Login()
login_screen.mainloop()
