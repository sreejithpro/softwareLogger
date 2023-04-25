import csv
import datetime
import psutil
import win32api
import tkinter as tk
from tkinter import ttk

process_names = ["notepad.exe", "calc.exe", "explorer.exe"]  # Change this to the process names you want to monitor
log_file = "process_log.csv"  # Change this to the path of the log file on the network drive


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log_process(process_name, username):
    with open(log_file, "r", newline="") as f:
        reader = csv.reader(f)
        for line in reader:
            if line == [process_name, username, ""]:
                return
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([process_name, username, get_current_time()])


def remove_process(process_name, username):
    with open(log_file, "r", newline="") as f:
        reader = csv.reader(f)
        lines = [line for line in reader if line != [process_name, username, ""]]
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def check_processes():
    running_processes = {}
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.name() in process_names:
            running_processes[proc.name()] = running_processes.get(proc.name(), set())
            running_processes[proc.name()].add(proc.username())
            username = win32api.GetUserName()
            if username not in running_processes[proc.name()]:
                log_process(proc.name(), username)
    for process_name in process_names:
        for child in tree.get_children():
            if child[0] == process_name and child[1] not in running_processes.get(process_name, set()):
                tree.delete(child)
                remove_process(process_name, child[1])
        for username in running_processes.get(process_name, set()):
            if not tree.exists((process_name, username)):
                tree.insert("", "end", (process_name, username), text=process_name, values=(username, get_current_time()))
            else:
                tree.set((process_name, username), 2, get_current_time())
    root.after(1000, check_processes)


root = tk.Tk()
root.title("Process Tracker")

tree = ttk.Treeview(root, columns=["#1", "#2", "#3"], show="headings")
tree.heading("#1", text="Process Name")
tree.heading("#2", text="User Name")
tree.heading("#3", text="Start Time")
tree.column("#1", width=100, anchor="w")
tree.column("#2", width=200, anchor="w")
tree.column("#3", width=200, anchor="w")
tree.pack(padx=10, pady=10)

root.after(1000, check_processes)

root.mainloop()