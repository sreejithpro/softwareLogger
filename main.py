import psutil

process_names = ["notepad.exe", "calc.exe", "explorer.exe"]  # Change this to the process names you want to monitor

def check_processes():
    running_processes = []
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] in process_names:
            running_processes.append(proc.info['name'])
    if len(running_processes) > 0:
        print(f"The following processes are running: {', '.join(running_processes)}")

while True:
    check_processes()
    # Adjust the sleep time as necessary to reduce CPU usage
    time.sleep(1)
