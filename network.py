import os
import paramiko
import subprocess

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


def get_mac_address(ip):
    """Retrieve the MAC address of the target system."""
    try:
        arp_result = subprocess.check_output(f"arp -n {ip}", shell=True, text=True)
        for line in arp_result.splitlines():
            if ip in line:
                return line.split()[2]
    except Exception as e:
        return f"Error retrieving MAC address: {e}"
    return "MAC address not found"


def ssh_and_execute(ip):
    """Connect to the target system via SSH and run commands."""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        commands = ["hostname", "hostname -I"]
        results = []

        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            results.append(stdout.read().decode().strip())

        mac_address = get_mac_address(ip)
        results.append(mac_address)

        client.close()
        return results
    except Exception as e:
        return [f"SSH connection failed: {e}"]


def main():
    if not os.path.exists(IP_LIST_FILE):
        print(f"IP list file '{IP_LIST_FILE}' not found.")
        return

    with open(IP_LIST_FILE, "r") as file:
        ip_list = file.read().splitlines()

    with open(OUTPUT_FILE, "w") as output:
        output.write("IP Address, Hostname, IP Info, MAC Address\n")
        for ip in ip_list:
            if is_reachable(ip):
                print(f"{ip} is reachable. Connecting via SSH...")
                results = ssh_and_execute(ip)
                output.write(f"{ip}, {', '.join(results)}\n")
            else:
                print(f"{ip} is not reachable.")
                output.write(f"{ip}, Unreachable\n")

    print(f"Output stored in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
