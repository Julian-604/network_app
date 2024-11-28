import os
import paramiko
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Predefined SSH credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# Input and output files
IP_LIST_FILE = "ip_list.txt"
OUTPUT_FILE = "output.txt"


def is_reachable(ip):
    """Check if the target IP is reachable using ping."""
    response = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0


def ssh_and_execute(ip, commands):
    """Connect to the target system via SSH and run custom commands."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        results = []
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            results.append(stdout.read().decode().strip())

        client.close()
        return f"{ip}, {', '.join(results)}"
    except Exception as e:
        return f"{ip}, SSH connection failed: {e}"


def process_ip(ip, commands):
    """Check reachability and execute SSH commands for a single IP."""
    if is_reachable(ip):
        print(f"{ip} is reachable. Connecting via SSH...")
        return ssh_and_execute(ip, commands)
    else:
        print(f"{ip} is not reachable.")
        return f"{ip}, Unreachable"


def main():
    if not os.path.exists(IP_LIST_FILE):
        print(f"IP list file '{IP_LIST_FILE}' not found.")
        return

    # Prompt for commands from the user
    commands = input("Enter the commands to execute (comma-separated): ").split(",")

    with open(IP_LIST_FILE, "r") as file:
        ip_list = file.read().splitlines()

    with open(OUTPUT_FILE, "w") as output:
        output.write("IP Address, Command Results\n")

        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust workers as needed
            results = executor.map(lambda ip: process_ip(ip, commands), ip_list)

        for result in results:
            output.write(f"{result}\n")

    print(f"Output stored in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
