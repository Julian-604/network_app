from netmiko import ConnectHandler
import time

# List of switch IP addresses
switch_ips = [
    '192.168.1.1',
    '192.168.1.2',
    '192.168.1.3',
    # Add all other switch IPs here
]

# Single username and password for all switches
username = 'admin'  # Replace with your actual username
password = 'password123'  # Replace with your actual password

# Command to run on all switches
command = 'show version'  # Replace with the command you want to run

# Loop through all switches and execute the command
for ip in switch_ips:
    try:
        # Define device connection details
        device = {
            'device_type': 'cisco_ios',  # For Cisco IOS devices
            'host': ip,
            'username': username,
            'password': password,
        }

        # Establish SSH connection to the switch
        connection = ConnectHandler(**device)

        # Send the command to the switch and capture the output
        output = connection.send_command(command)

        # Print the output from the switch
        print(f"Output from {ip}:\n{output}\n")

        # Close the connection
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip}: {str(e)}")

    # Optional: Add a delay to prevent overwhelming the switches with requests
    time.sleep(1)  # Adjust as needed
