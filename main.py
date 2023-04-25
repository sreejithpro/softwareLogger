import psutil
import win32api
import tkinter as tk
import os

process_name = "notepad.exe"  # Change this to the process name you want to monitor
log_file = r'P:\INBLC\W&E\GE\Geotech\Shared Documents\E. Softwares\Software Tracker\process_log.txt'  # Change this to the path of the log file on the network drive


def check_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.name() == process_name:
            username = win32api.GetUserName()
            message = f"User {username} has started using {process_name}."
            with open(log_file, "a") as f:
                f.write(message + "\n")
            label.config(text=message)
            break
    else:
        message = f"No process with the name {process_name} is running."
        label.config(text=message)
    root.after(1000, check_process)


def read_log_file():
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_data = f.read()
    else:
        log_data = "Log file not found."
        with open(log_file, "w") as f:
            pass
    return log_data


root = tk.Tk()
root.title("Process Tracker")

label = tk.Label(root, text="Checking process...")
label.pack(padx=10, pady=10)

log_label = tk.Label(root, text=read_log_file())
log_label.pack(padx=10, pady=10)

root.after(1000, check_process)

root.mainloop()
