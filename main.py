import csv
import psutil
import time

process_names = ["notepad.exe", "wordpad.exe", "explorer.exe"]  # Change this to the process names you want to monitor
log_file = "process_log.csv"  # Change this to the path of the log file on the network drive
max_rows = 100  # Change this to the maximum number of rows to keep in the log file

previous_running_processes = []


def check_processes():
    global previous_running_processes
    running_processes = []
    for proc in psutil.process_iter(['name', 'username']):
        if proc.info['name'] in process_names:
            running_processes.append((proc.info['name'], proc.info['username']))
    if running_processes != previous_running_processes:
        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)
            for process_name, username in running_processes:
                writer.writerow([process_name, username, time.strftime("%Y-%m-%d %H:%M:%S")])
        previous_running_processes = running_processes
        with open(log_file, "r", newline="") as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
        if len(rows) > max_rows:
            with open(log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows[-max_rows:])


while True:
    check_processes()
    # Adjust the sleep time as necessary to reduce CPU usage
    time.sleep(1)
