import os
import psutil
import win32api
import tkinter as tk

process_names = ["notepad.exe", "calculator.exe", "explorer.exe"]  # Change this to the process names you want to monitor
log_file = "process_log.txt"  # Change this to the path of the log file on the network drive
max_lines = 50  # Change this to the maximum number of lines to keep in the log file


def check_processes():
    running_processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.name() in process_names:
            running_processes.append(proc.name())
            username = win32api.GetUserName()
            message = f"User {username} has started using {proc.name()}."
            with open(log_file, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                f.write(message + "\n")
                f.writelines(lines)
                f.truncate(max_lines * (len(lines) // max_lines + 1))
    if running_processes:
        message = f"User {username} is currently using the following processes: {', '.join(running_processes)}."
        label.config(text=message)
    else:
        message = f"No processes are running."
        label.config(text=message)
    root.after(1000, check_processes)


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

label = tk.Label(root, text="Checking processes...")
label.pack(padx=10, pady=10)

log_label = tk.Label(root, text=read_log_file())
log_label.pack(padx=10, pady=10)

root.after(1000, check_processes)

root.mainloop()