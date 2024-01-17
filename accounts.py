import tkinter
from tkinter import ttk
import customtkinter as ctk
import tkinter.messagebox as messagebox
from utils.database import Database
import hashlib


class Accounts(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Accounts")
        self.geometry("920x480")
        self.grid_columnconfigure((0, 0), weight=1)

        # Widgets
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.add_account = ctk.CTkButton(
            self.button_frame, text="+ Add account", command=self.add_account_cmd
        )
        self.edit_account = ctk.CTkButton(
            self.button_frame, text="Edit account", command=self.edit_account_cmd
        )
        self.delete_account = ctk.CTkButton(
            self.button_frame,
            text="Delete account",
            command=self.delete_account_cmd,
            fg_color="red",
            hover_color="darkred",
        )
        self.accounts_table = ttk.Treeview(
            self,
            columns=("employee_number", "firstname", "middlename", "lastname"),
            show="headings",
            selectmode="browse",
        )

        self.accounts_table.heading("employee_number", text="Employee no.")
        self.accounts_table.heading("firstname", text="First name")
        self.accounts_table.heading("middlename", text="Middle name")
        self.accounts_table.heading("lastname", text="Last name")

        self.populate_accounts_table()

        self.button_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.add_account.grid(row=0, column=0, padx=(0, 10))
        self.edit_account.grid(row=0, column=1, padx=(0, 10))
        self.delete_account.grid(row=0, column=2)
        self.accounts_table.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")

    def populate_accounts_table(self):
        db = Database()
        self.accounts = db.get_all("login")

        # Clear existing data
        self.accounts_table.delete(*self.accounts_table.get_children())

        for account in self.accounts:
            self.accounts_table.insert(
                "",
                "end",
                values=(
                    account["employee_number"],
                    account["first_name"],
                    account["middle_name"],
                    account["last_name"],
                ),
            )

    def add_account_cmd(self):
        add_account_form = AddAccountForm(self, self.populate_accounts_table)
        add_account_form.grab_set()

    def edit_account_cmd(self):
        selected_account = self.get_selected_account()
        if selected_account:
            edit_account_form = EditAccountForm(
                self, selected_account, self.populate_accounts_table
            )
            edit_account_form.grab_set()
        else:
            messagebox.showwarning(
                "No Account Selected", "Please select an account to edit."
            )

    def delete_account_cmd(self):
        selected_account = self.get_selected_account()
        if selected_account:
            confirmation = messagebox.askyesno(
                "Confirm Deletion", "Do you really want to delete this account?"
            )
            if confirmation:
                db = Database()
                db.delete_login_info(selected_account[0])
                print(f"Delete {selected_account}")
                self.populate_accounts_table()
        else:
            messagebox.showwarning(
                "No Account Selected", "Please select an account to delete."
            )

    def get_selected_account(self):
        selected = self.accounts_table.item(self.accounts_table.focus())["values"]

        return selected if selected else None


class AddAccountForm(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.geometry("400x300")
        self.title("Add Account")
        self.grid_columnconfigure((0, 1), weight=5)
        self.grid_columnconfigure((1, 0), weight=1)

        # Form widgets
        self.employee_number_label = ctk.CTkLabel(self, text="Employee Number")
        self.employee_number_entry = ctk.CTkEntry(self)

        self.first_name_label = ctk.CTkLabel(self, text="First Name")
        self.first_name_entry = ctk.CTkEntry(self)

        self.middle_name_label = ctk.CTkLabel(self, text="Middle Name")
        self.middle_name_entry = ctk.CTkEntry(self)

        self.last_name_label = ctk.CTkLabel(self, text="Last Name")
        self.last_name_entry = ctk.CTkEntry(self)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_entry = ctk.CTkEntry(self, show="*")

        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_account)

        # Grid layout
        self.employee_number_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.employee_number_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.middle_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.middle_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.last_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.last_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.password_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.save_button.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

    def save_account(self):
        employee_number = self.employee_number_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        password = self.password_entry.get()
        md5_password = hashlib.md5(password.encode()).hexdigest()

        # Validate the data
        if not validate_account_data(employee_number, first_name, password):
            return

        # Save the account to the database or perform any other necessary actions
        db = Database()
        db.insert_login_info(
            {
                "employee_number": employee_number,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "hash": md5_password,
            }
        )

        self.callback()
        self.destroy()


def validate_account_data(employee_number, first_name, password):
    if not (employee_number and first_name and password):
        messagebox.showwarning(
            "Missing Fields",
            "Please fill out all the fields before saving the account.",
        )
        return False

    if not employee_number.isdigit() and len(employee_number) != 9:
        messagebox.showwarning(
            "Invalid Employee Number",
            "Please enter a valid employee number.",
        )
        return False

    if len(password) < 8:
        messagebox.showwarning(
            "Invalid Password",
            "Password must be at least 8 characters long.",
        )
        return False

    return True


class EditAccountForm(ctk.CTkToplevel):
    def __init__(self, parent, account, callback):
        super().__init__(parent)
        self.callback = callback
        self.account = account
        self.geometry("400x300")
        self.title("Edit Account")
        self.grid_columnconfigure((0, 1), weight=5)
        self.grid_columnconfigure((1, 0), weight=1)

        # Form widgets
        self.employee_number_label = ctk.CTkLabel(self, text="Employee Number")
        self.employee_number_entry = ctk.CTkEntry(self)

        self.first_name_label = ctk.CTkLabel(self, text="First Name")
        self.first_name_entry = ctk.CTkEntry(self)

        self.middle_name_label = ctk.CTkLabel(self, text="Middle Name")
        self.middle_name_entry = ctk.CTkEntry(self)

        self.last_name_label = ctk.CTkLabel(self, text="Last Name")
        self.last_name_entry = ctk.CTkEntry(self)

        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_entry = ctk.CTkEntry(self, show="*")

        self.save_button = ctk.CTkButton(
            self, text="Update", command=self.update_account
        )

        # Grid layout
        self.employee_number_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.employee_number_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.middle_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.middle_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.last_name_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.last_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.password_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.save_button.grid(
            row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )

        # Populate form with existing account data
        self.employee_number_entry.insert(0, account[0])
        self.first_name_entry.insert(0, account[1])
        self.middle_name_entry.insert(0, account[2])
        self.last_name_entry.insert(0, account[3])

    def update_account(self):
        employee_number = self.employee_number_entry.get()
        first_name = self.first_name_entry.get()
        middle_name = self.middle_name_entry.get()
        last_name = self.last_name_entry.get()
        password = self.password_entry.get()
        md5_password = hashlib.md5(password.encode()).hexdigest()

        # Validate the data
        if not validate_account_data(employee_number, first_name, password):
            return

        # Save the account to the database or perform any other necessary actions
        db = Database()
        db.update_login_info(
            employee_number,
            {
                "employee_number": employee_number,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "hash": md5_password,
            },
        )

        print(f"Update {self.account}")
        self.callback()
        self.destroy()


accounts = Accounts()
accounts.mainloop()
