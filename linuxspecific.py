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


def ssh_and_execute(ip, primary_commands, fallback_commands):
    """Connect to the target system via SSH and execute commands."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        results = []

        # Execute primary commands
        for command in primary_commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            results.append(f"Command: {command}\nOutput: {output}\nError: {error}")

            if "failed" in error.lower() or stdout.channel.recv_exit_status() != 0:
                results.append("Primary command failed. Executing fallback commands.")
                break
        else:
            client.close()
            return f"{ip},\n" + "\n".join(results)

        # Execute fallback commands if primary commands failed
        for command in fallback_commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            results.append(f"Command: {command}\nOutput: {output}\nError: {error}")

        client.close()
        return f"{ip},\n" + "\n".join(results)

    except Exception as e:
        return f"{ip}, SSH connection failed: {e}"


def process_ip(ip, primary_commands, fallback_commands):
    """Check reachability and execute SSH commands for a single IP."""
    if is_reachable(ip):
        print(f"{ip} is reachable. Connecting via SSH...")
        return ssh_and_execute(ip, primary_commands, fallback_commands)
    else:
        print(f"{ip} is not reachable.")
        return f"{ip}, Unreachable"


def main():
    if not os.path.exists(IP_LIST_FILE):
        print(f"IP list file '{IP_LIST_FILE}' not found.")
        return

    # Define primary and fallback commands
    primary_commands = [
        "sudo -S apt update",
        "sudo -S apt upgrade -y"
    ]
    fallback_commands = [
        "sudo -S apt install -f",
        "sudo -S apt upgrade -y"
    ]

    with open(IP_LIST_FILE, "r") as file:
        ip_list = file.read().splitlines()

    with open(OUTPUT_FILE, "w") as output:
        output.write("Results:\n\n")

        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(
                lambda ip: process_ip(ip, primary_commands, fallback_commands),
                ip_list
            )

        for result in results:
            output.write(f"{result}\n\n")

    print(f"Output stored in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
