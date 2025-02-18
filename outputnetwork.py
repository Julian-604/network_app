import argparse
from netmiko import ConnectHandler

# Predefined username and password
USERNAME = 'admin'  # Replace with your actual username
PASSWORD = 'password123'  # Replace with your actual password

def run_command_on_switch(switch_ip, command, output_file):
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

        # Write the output to a text file
        with open(output_file, 'a') as file:
            file.write(f"Output from {switch_ip}:\n{output}\n\n")

        # Close the connection
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {switch_ip}: {str(e)}")


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Run a command on a Cisco switch and store the output in a file.")
    parser.add_argument('switch_ip', type=str, help="IP address of the switch")
    parser.add_argument('command', type=str, help="Command to run on the switch")
    parser.add_argument('output_file', type=str, help="File to store the output")

    # Parse the arguments
    args = parser.parse_args()

    # Run the command on the switch and store output in the file
    run_command_on_switch(args.switch_ip, args.command, args.output_file)

if __name__ == "__main__":
    main()
