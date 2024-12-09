import argparse
import re
from netmiko import ConnectHandler

# Predefined username and password
USERNAME = 'admin'  # Replace with your actual username
PASSWORD = 'password123'  # Replace with your actual password

def run_command_on_switch(switch_ip, command):
    try:
        # Define device connection details (using predefined username and password)
        device = {
            'device_type': 'cisco_ios',  # For Cisco IOS devices
            'host': switch_ip,
            'username': USERNAME,
            'password': PASSWORD,
        }

        # Establish SSH connection to the switch
        connection = ConnectHandler(**device)

        # Send the command to the switch and capture the output
        output = connection.send_command(command)

        # Use regex to find the serial number in the output
        serial_number_match = re.search(r"System serial number\s*:\s*(\S+)", output)
        
        if serial_number_match:
            serial_number = serial_number_match.group(1)
            print(f"Switch IP: {switch_ip}, Serial Number: {serial_number}")
        else:
            print(f"Serial number not found for {switch_ip}")

        # Close the connection
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {switch_ip}: {str(e)}")


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run a command on a Cisco switch and get filtered output.")
    parser.add_argument('switch_ip', type=str, help="IP address of the switch")
    parser.add_argument('command', type=str, help="Command to run on the switch")

    # Parse the arguments
    args = parser.parse_args()

    # Run the command on the switch
    run_command_on_switch(args.switch_ip, args.command)

if __name__ == "__main__":
    main()