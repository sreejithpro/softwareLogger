import os
import psutil
import win32api
import tkinter as tk
from tkinter import ttk

process_names = ["notepad.exe", "calc.exe", "explorer.exe"]  # Change this to the process names you want to monitor
log_file = "process_log.txt"  # Change this to the path of the log file on the network drive
max_lines = 100  # Change this to the maximum number of lines to keep in the log file


def check_processes():
    running_processes = {}
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.name() in process_names:
            running_processes[proc.name()] = running_processes.get(proc.name(), set())
            running_processes[proc.name()].add(proc.username())
            username = win32api.GetUserName()
            message = f"User {username} has started using {proc.name()}."
            with open(log_file, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                f.write(message + "\n")
                f.writelines(lines)
                f.truncate(max_lines * (len(lines) // max_lines + 1))
    for process_name in process_names:
        users = sorted(running_processes.get(process_name, set()))
        if not tree.exists(process_name):
            tree.insert("", "end", process_name, text=process_name)
        for i, user in enumerate(users):
            tree.set(process_name, i + 1, user)
        for j in range(len(users), tree.column("#") - 1):
            tree.set(process_name, j + 1, "")
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

tree = ttk.Treeview(root, columns=["#" + str(i) for i in range(len(process_names) + 1)], show="headings")
tree.heading("#0", text="")
for i, process_name in enumerate(process_names):
    tree.heading("#" + str(i + 1), text=process_name)
tree.column("#0", width=100, anchor="w")
for i in range(len(process_names)):
    tree.column("#" + str(i + 1), width=200, anchor="w")
tree.pack(padx=10, pady=10)

log_label = tk.Label(root, text=read_log_file())
log_label.pack(padx=10, pady=10)

root.after(1000, check_processes)

root.mainloop()
