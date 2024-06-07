import tkinter as tk
from tkinter import messagebox
import subprocess

def check_credentials():
    if username_entry.get() == "admin" and password_entry.get() == "123456":
        # Close the login window
        window.destroy()

        # Create the attendance window
        attendance_window = tk.Tk()
        attendance_window.title("Attendance System")
        attendance_window.geometry('400x400')
        attendance_window.configure(bg='#333333')

        frame = tk.Frame(attendance_window, bg='#333333')
        system_label = tk.Label(frame, text="Attendance System", bg='#333333', fg="#FFFFFF", font=(30))
        register_label = tk.Label(frame, text="Register", bg='#333333', fg="#FFFFFF")
        register_entry = tk.Entry(frame)
        register_btn = tk.Button(frame, text="Submit", bg="#FF3399", command=lambda: call_dataset_script(register_entry.get()))
        remove_label = tk.Label(frame, text="Remove", bg='#333333', fg="#FFFFFF")
        remove_entry = tk.Entry(frame)
        remove_btn = tk.Button(frame, text="Submit", bg="#FF3399", command=lambda: call_remove_script(remove_entry.get()))
        att_btn = tk.Button(frame, text="Attendance", bg="#FF3399", command=call_attendance_script)

        # Placing
        system_label.grid(row=0, column=0, columnspan=3, pady=40)
        register_label.grid(row=1, column=0, pady=10)
        register_entry.grid(row=1, column=1, pady=10)
        register_btn.grid(row=1, column=2, pady=10, padx=10)
        remove_label.grid(row=2, column=0, pady=10)
        remove_entry.grid(row=2, column=1, pady=10)
        remove_btn.grid(row=2, column=2, pady=10, padx=10)
        att_btn.grid(row=3, column=0, columnspan=3, pady=30)
        frame.pack()

        attendance_window.mainloop()
    else:
        messagebox.showinfo("Login info", "Incorrect credentials")

def call_remove_script(name):
    if name:
        result = subprocess.run(['python', 'remove.py', name], capture_output=True, text=True)
        messagebox.showinfo("Remove info", result.stdout)
    else:
        messagebox.showinfo("Remove info", "Please enter a name.")

def call_dataset_script(name):
    if name:
        result = subprocess.run(['python', 'Dataset.py', name], capture_output=True, text=True)
        messagebox.showinfo("Register info", result.stdout)
    else:
        messagebox.showinfo("Register info", "Please enter a name.")

def call_attendance_script():
    result = subprocess.run(['python', 'main.py'], capture_output=True, text=True)
    messagebox.showinfo("Attendance info", result.stdout)

window = tk.Tk()
window.title("Login Form")
window.geometry('400x400')
window.configure(bg='#333333')

frame = tk.Frame(window, bg='#333333')
# Creating widgets
login_label = tk.Label(frame, text="Login", bg='#333333', fg="#FFFFFF", font=(30))
username_label = tk.Label(frame, text="Username", bg='#333333', fg="#FFFFFF")
username_entry = tk.Entry(frame)
password_label = tk.Label(frame, text="Password", bg='#333333', fg="#FFFFFF")
password_entry = tk.Entry(frame, show="*")
login_btn = tk.Button(frame, text="Login", command=check_credentials, bg="#FF3399")

# Placing widgets on screen 
login_label.grid(row=0, column=0, columnspan=2, pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=10)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=10)
login_btn.grid(row=3, column=0, columnspan=2, pady=30)
frame.pack()

window.mainloop()


