import os
from tkinter import *
from tkinter import messagebox, filedialog
import random  # Used for simulating features like credit score
import time     # Used for time-related features

def loginclk():
    username = un_entry.get()
    password = pw_entry.get()
    filename = username + ".txt"
    try:
        with open(filename, "r") as f:
            stored_password = f.readline().strip()
        if stored_password == password:
            root.destroy()
            main_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    except FileNotFoundError:
        messagebox.showerror("Login Failed", "Account does not exist.")

def signUp():
    def register():
        username = un_entry.get()
        password = pw_entry.get()
        filename = username + ".txt"
        if os.path.exists(filename):
            messagebox.showerror("Sign Up Failed", "Username already exists.")
        else:
            with open(filename, "w") as f:
                f.write(password + "\n")
                f.write("0.00")  # Starting balance
            messagebox.showinfo("Sign Up Successful", "Account created successfully.")
            signUpWindow.destroy()

    signUpWindow = Toplevel(root)
    signUpWindow.title("Sign Up")
    signUpWindow.geometry("300x200")
    signUpWindow.configure(bg="lightblue")

    Label(signUpWindow, text="Username:", font=('Comic Sans MS', 12), bg="lightblue").pack(pady=10)
    un_entry = Entry(signUpWindow, font=('Comic Sans MS', 12))
    un_entry.pack(pady=10)

    Label(signUpWindow, text="Password:", font=('Comic Sans MS', 12), bg="lightblue").pack(pady=10)
    pw_entry = Entry(signUpWindow, show="*", font=('Comic Sans MS', 12))
    pw_entry.pack(pady=10)

    Button(signUpWindow, text="Register", width=20, height=2, command=register).pack(pady=10)
    Button(signUpWindow, text="Cancel", width=20, height=2, command=signUpWindow.destroy).pack(pady=10)

def main_window(username):
    def deposit(username):
        """Handle deposit."""
        def submit_deposit():
            amount = deposit_amount_entry.get()
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                filename = username + ".txt"
                with open(filename, "r") as f:
                    password = f.readline().strip()
                    balance = float(f.readline().strip())
                balance += amount
                with open(filename, "w") as f:
                    f.write(password + "\n")
                    f.write(f"{balance:.2f}")
                with open(username + "_history.txt", "a") as f:
                    f.write(f"Deposited {amount:.2f}\n")
                messagebox.showinfo("Success", f"Deposited {amount:.2f} successfully.")
                deposit_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        deposit_window = Toplevel(main_window)
        deposit_window.title("Deposit")
        deposit_window.configure(bg="lightyellow")

        Label(deposit_window, text="Enter amount to deposit:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        deposit_amount_entry = Entry(deposit_window, font=('Comic Sans MS', 12))
        deposit_amount_entry.pack(pady=10)
        Button(deposit_window, text="Submit", width=20, height=2, command=submit_deposit).pack(pady=10)
        Button(deposit_window, text="Cancel", width=20, height=2, command=deposit_window.destroy).pack(pady=10)

    def withdraw(username):
        """Handle withdrawal."""
        def submit_withdrawal():
            amount = withdraw_amount_entry.get()
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                filename = username + ".txt"
                with open(filename, "r") as f:
                    password = f.readline().strip()
                    balance = float(f.readline().strip())
                if amount > balance:
                    raise ValueError("Insufficient balance.")
                balance -= amount
                with open(filename, "w") as f:
                    f.write(password + "\n")
                    f.write(f"{balance:.2f}")
                with open(username + "_history.txt", "a") as f:
                    f.write(f"Withdrew {amount:.2f}\n")
                messagebox.showinfo("Success", f"Withdrew {amount:.2f} successfully.")
                withdraw_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        withdraw_window = Toplevel(main_window)
        withdraw_window.title("Withdraw")
        withdraw_window.configure(bg="lightyellow")

        Label(withdraw_window, text="Enter amount to withdraw:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        withdraw_amount_entry = Entry(withdraw_window, font=('Comic Sans MS', 12))
        withdraw_amount_entry.pack(pady=10)
        Button(withdraw_window, text="Submit", width=20, height=2, command=submit_withdrawal).pack(pady=10)
        Button(withdraw_window, text="Cancel", width=20, height=2, command=withdraw_window.destroy).pack(pady=10)

    def transfer_funds(username):
        """Handle fund transfers."""
        def transfer_amount():
            recipient = recipient_entry.get()
            amount = amount_entry.get()
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                filename = username + ".txt"
                with open(filename, "r") as f:
                    password = f.readline().strip()
                    balance = float(f.readline().strip())
                if amount > balance:
                    raise ValueError("Insufficient balance.")
                balance -= amount
                with open(filename, "w") as f:
                    f.write(password + "\n")
                    f.write(f"{balance:.2f}")
                # Simulate recipient account
                recipient_file = recipient + ".txt"
                if os.path.exists(recipient_file):
                    with open(recipient_file, "r") as f:
                        recipient_password = f.readline().strip()
                        recipient_balance = float(f.readline().strip())
                    recipient_balance += amount
                    with open(recipient_file, "w") as f:
                        f.write(recipient_password + "\n")
                        f.write(f"{recipient_balance:.2f}")
                    with open(username + "_history.txt", "a") as f:
                        f.write(f"Transferred {amount:.2f} to {recipient}\n")
                    messagebox.showinfo("Success", f"Transferred {amount:.2f} to {recipient} successfully.")
                else:
                    raise ValueError("Recipient account does not exist.")
                transfer_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        transfer_window = Toplevel(main_window)
        transfer_window.title("Transfer Funds")
        transfer_window.configure(bg="lightyellow")

        Label(transfer_window, text="Enter recipient username:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        recipient_entry = Entry(transfer_window, font=('Comic Sans MS', 12))
        recipient_entry.pack(pady=10)

        Label(transfer_window, text="Enter amount to transfer:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        amount_entry = Entry(transfer_window, font=('Comic Sans MS', 12))
        amount_entry.pack(pady=10)

        Button(transfer_window, text="Submit", width=20, height=2, command=transfer_amount).pack(pady=10)
        Button(transfer_window, text="Cancel", width=20, height=2, command=transfer_window.destroy).pack(pady=10)

    def account_summary(username):
        """Show account summary including balance."""
        filename = username + ".txt"
        try:
            with open(filename, "r") as f:
                password = f.readline().strip()
                balance = float(f.readline().strip())
            summary_window = Toplevel(main_window)
            summary_window.title("Account Summary")
            summary_window.configure(bg="lightyellow")
            Label(summary_window, text=f"Username: {username}", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
            Label(summary_window, text=f"Balance: {balance:.2f}", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
            Button(summary_window, text="OK", width=20, height=2, command=summary_window.destroy).pack(pady=10)
        except FileNotFoundError:
            messagebox.showerror("Error", "Account file not found.")

    def transaction_history(username):
        """Show transaction history."""
        history_file = username + "_history.txt"
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                history = f.read()
            history_window = Toplevel(main_window)
            history_window.title("Transaction History")
            history_window.configure(bg="lightyellow")
            text_box = Text(history_window, height=20, width=60, font=('Comic Sans MS', 12))
            text_box.insert(END, history)
            text_box.pack(pady=10)
            Button(history_window, text="OK", width=20, height=2, command=history_window.destroy).pack(pady=10)
        else:
            messagebox.showerror("Error", "No transaction history found.")

    def pay_bills(username):
        """Pay bills."""
        def pay():
            bill_type = bill_type_var.get()
            amount = bill_amount_entry.get()
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                filename = username + ".txt"
                with open(filename, "r") as f:
                    password = f.readline().strip()
                    balance = float(f.readline().strip())
                if amount > balance:
                    raise ValueError("Insufficient balance.")
                balance -= amount
                with open(filename, "w") as f:
                    f.write(password + "\n")
                    f.write(f"{balance:.2f}")
                with open(username + "_history.txt", "a") as f:
                    f.write(f"Paid {amount:.2f} for {bill_type}\n")
                messagebox.showinfo("Success", f"Paid {amount:.2f} for {bill_type} successfully.")
                pay_window.destroy()
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        bill_types = ["Electricity", "Water", "Internet", "Rent"]
        pay_window = Toplevel(main_window)
        pay_window.title("Pay Bills")
        pay_window.configure(bg="lightyellow")

        Label(pay_window, text="Select bill type:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        bill_type_var = StringVar()
        for bill_type in bill_types:
            Radiobutton(pay_window, text=bill_type, variable=bill_type_var, value=bill_type, bg="lightyellow").pack(anchor=W)

        Label(pay_window, text="Enter amount to pay:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        bill_amount_entry = Entry(pay_window, font=('Comic Sans MS', 12))
        bill_amount_entry.pack(pady=10)
        Button(pay_window, text="Submit", width=20, height=2, command=pay).pack(pady=10)
        Button(pay_window, text="Cancel", width=20, height=2, command=pay_window.destroy).pack(pady=10)

    def settings(username):
        """Open settings."""
        def change_theme():
            theme = theme_var.get()
            if theme == "Light":
                main_window.configure(bg="lightyellow")
            elif theme == "Dark":
                main_window.configure(bg="darkgrey")

        def update_profile():
            new_username = new_username_entry.get()
            if new_username:
                old_file = username + ".txt"
                new_file = new_username + ".txt"
                os.rename(old_file, new_file)
                messagebox.showinfo("Profile Updated", "Username updated successfully.")
                settings_window.destroy()

        settings_window = Toplevel(main_window)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(bg="lightyellow")

        Label(settings_window, text="Change Theme:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        theme_var = StringVar(value="Light")
        Radiobutton(settings_window, text="Light", variable=theme_var, value="Light", bg="lightyellow").pack(anchor=W)
        Radiobutton(settings_window, text="Dark", variable=theme_var, value="Dark", bg="lightyellow").pack(anchor=W)
        Button(settings_window, text="Change Theme", width=20, height=2, command=change_theme).pack(pady=10)

        Label(settings_window, text="Update Username:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        new_username_entry = Entry(settings_window, font=('Comic Sans MS', 12))
        new_username_entry.pack(pady=10)
        Button(settings_window, text="Update Username", width=20, height=2, command=update_profile).pack(pady=10)

    def change_theme():
        """Change the application theme."""
        def apply_theme():
            theme = theme_var.get()
            if theme == "Light":
                main_window.configure(bg="lightyellow")
            elif theme == "Dark":
                main_window.configure(bg="darkgrey")

        theme_window = Toplevel(main_window)
        theme_window.title("Change Theme")
        theme_window.geometry("300x200")
        theme_window.configure(bg="lightyellow")

        Label(theme_window, text="Select Theme:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        theme_var = StringVar(value="Light")
        Radiobutton(theme_window, text="Light", variable=theme_var, value="Light", bg="lightyellow").pack(anchor=W)
        Radiobutton(theme_window, text="Dark", variable=theme_var, value="Dark", bg="lightyellow").pack(anchor=W)
        Button(theme_window, text="Apply", width=20, height=2, command=apply_theme).pack(pady=10)
        Button(theme_window, text="Cancel", width=20, height=2, command=theme_window.destroy).pack(pady=10)

    def show_interest():
        """Calculate interest."""
        def calculate():
            try:
                principal = float(principal_entry.get())
                rate = float(rate_entry.get())
                time = float(time_entry.get())
                interest = principal * (rate / 100) * time
                interest_label.config(text=f"Interest: {interest:.2f}")
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        interest_window = Toplevel(main_window)
        interest_window.title("Interest Calculator")
        interest_window.configure(bg="lightyellow")

        Label(interest_window, text="Principal:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        principal_entry = Entry(interest_window, font=('Comic Sans MS', 12))
        principal_entry.pack(pady=10)

        Label(interest_window, text="Rate of Interest (%):", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        rate_entry = Entry(interest_window, font=('Comic Sans MS', 12))
        rate_entry.pack(pady=10)

        Label(interest_window, text="Time (years):", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        time_entry = Entry(interest_window, font=('Comic Sans MS', 12))
        time_entry.pack(pady=10)

        Button(interest_window, text="Calculate", width=20, height=2, command=calculate).pack(pady=10)
        interest_label = Label(interest_window, text="", font=('Comic Sans MS', 12), bg="lightyellow")
        interest_label.pack(pady=10)
        Button(interest_window, text="Cancel", width=20, height=2, command=interest_window.destroy).pack(pady=10)

    def export_history(username):
        """Export transaction history to a file."""
        history_file = username + "_history.txt"
        try:
            with open(history_file, "r") as f:
                transactions = f.read()
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(transactions)
                messagebox.showinfo("Success", "Transaction history exported successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction history file not found.")

    def currency_converter():
        """Convert currency."""
        def convert():
            try:
                amount = float(amount_entry.get())
                rate = float(rate_entry.get())
                converted_amount = amount * rate
                result_label.config(text=f"Converted Amount: {converted_amount:.2f}")
            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        converter_window = Toplevel(main_window)
        converter_window.title("Currency Converter")
        converter_window.configure(bg="lightyellow")

        Label(converter_window, text="Enter amount:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        amount_entry = Entry(converter_window, font=('Comic Sans MS', 12))
        amount_entry.pack(pady=10)

        Label(converter_window, text="Enter exchange rate:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        rate_entry = Entry(converter_window, font=('Comic Sans MS', 12))
        rate_entry.pack(pady=10)

        Button(converter_window, text="Convert", width=20, height=2, command=convert).pack(pady=10)
        result_label = Label(converter_window, text="", font=('Comic Sans MS', 12), bg="lightyellow")
        result_label.pack(pady=10)
        Button(converter_window, text="Cancel", width=20, height=2, command=converter_window.destroy).pack(pady=10)

    def biometric_authentication():
        """Simulate biometric authentication."""
        def authenticate():
            # This is a placeholder. In real applications, biometric authentication would be more complex.
            if biometric_entry.get() == "correct_biometric_data":
                messagebox.showinfo("Success", "Biometric authentication successful.")
            else:
                messagebox.showerror("Failure", "Biometric authentication failed.")
            biometric_window.destroy()

        biometric_window = Toplevel(main_window)
        biometric_window.title("Biometric Authentication")
        biometric_window.geometry("300x200")
        biometric_window.configure(bg="lightyellow")

        Label(biometric_window, text="Enter biometric data:", font=('Comic Sans MS', 12), bg="lightyellow").pack(pady=10)
        biometric_entry = Entry(biometric_window, font=('Comic Sans MS', 12))
        biometric_entry.pack(pady=10)
        Button(biometric_window, text="Authenticate", width=20, height=2, command=authenticate).pack(pady=10)
        Button(biometric_window, text="Cancel", width=20, height=2, command=biometric_window.destroy).pack(pady=10)

    # Main application window
    main_window = Tk()
    main_window.title("Banking Application")
    main_window.geometry("800x600")
    main_window.configure(bg="lightyellow")

    # Create buttons
    Button(main_window, text="Deposit", width=20, height=2, command=lambda: deposit(username)).grid(row=0, column=0, padx=20, pady=10)
    Button(main_window, text="Withdraw", width=20, height=2, command=lambda: withdraw(username)).grid(row=0, column=1, padx=20, pady=10)
    Button(main_window, text="Transfer Funds", width=20, height=2, command=lambda: transfer_funds(username)).grid(row=0, column=2, padx=20, pady=10)
    Button(main_window, text="Account Summary", width=20, height=2, command=lambda: account_summary(username)).grid(row=0, column=3, padx=20, pady=10)

    Button(main_window, text="Transaction History", width=20, height=2, command=lambda: transaction_history(username)).grid(row=1, column=0, padx=20, pady=10)
    Button(main_window, text="Pay Bills", width=20, height=2, command=lambda: pay_bills(username)).grid(row=1, column=1, padx=20, pady=10)
    Button(main_window, text="Settings", width=20, height=2, command=lambda: settings(username)).grid(row=1, column=2, padx=20, pady=10)
    Button(main_window, text="Change Theme", width=20, height=2, command=change_theme).grid(row=1, column=3, padx=20, pady=10)

    Button(main_window, text="Interest Calculator", width=20, height=2, command=show_interest).grid(row=2, column=0, padx=20, pady=10)
    Button(main_window, text="Export History", width=20, height=2, command=lambda: export_history(username)).grid(row=2, column=1, padx=20, pady=10)
    Button(main_window, text="Currency Converter", width=20, height=2, command=currency_converter).grid(row=2, column=2, padx=20, pady=10)
    Button(main_window, text="Biometric Authentication", width=20, height=2, command=biometric_authentication).grid(row=2, column=3, padx=20, pady=10)

    # Show the main window
    main_window.mainloop()

# Main login window
root = Tk()
root.title("Login")
root.geometry("300x200")
root.configure(bg="lightblue")

Label(root, text="Username:", font=('Comic Sans MS', 12), bg="lightblue").pack(pady=10)
un_entry = Entry(root, font=('Comic Sans MS', 12))
un_entry.pack(pady=10)

Label(root, text="Password:", font=('Comic Sans MS', 12), bg="lightblue").pack(pady=10)
pw_entry = Entry(root, show="*", font=('Comic Sans MS', 12))
pw_entry.pack(pady=10)

Button(root, text="Login", width=20, height=2, command=loginclk).pack(pady=10)
Button(root, text="Sign Up", width=20, height=2, command=signUp).pack(pady=10)

root.mainloop()
