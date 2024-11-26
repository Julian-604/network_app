#!/bin/bash

# File containing the list of IP addresses (one per line)
IP_LIST="ips.txt"

# File containing the list of passwords (one per line)
PASSWORDS="passwords.txt"

# Output file
OUTPUT_FILE="ssh_output.txt"

# SSH username
USERNAME="your_user"

# Clear the output file before running the script
> "$OUTPUT_FILE"

# Iterate over each IP address
while read -r IP; do
    echo "Checking $IP..."

    # Check if the host is reachable
    if ping -c 1 -W 1 "$IP" &> /dev/null; then
        echo "$IP is reachable."

        # Flag to track if SSH was successful with a password
        SUCCESS=0  

        # Iterate over each password in the list
        while read -r PASSWORD; do
            # Try SSH connection using sshpass
            OUTPUT=$(sshpass -p "$PASSWORD" ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no $USERNAME@$IP "echo -n $(hostname) && echo ' ' $(hostname -I | awk '{print $1}')" 2>/dev/null)

            # If SSH connection is successful, log the output and break out of the password loop
            if [ $? -eq 0 ]; then
                echo "Success: $OUTPUT"
                echo "$OUTPUT" >> "$OUTPUT_FILE"
                SUCCESS=1
                break  # Stop checking further passwords
            fi
        done < "$PASSWORDS"

        # If no password worked, log the IP only
        if [ $SUCCESS -eq 0 ]; then
            echo "No valid password for $IP."
            echo "$IP" >> "$OUTPUT_FILE"
        fi
    else
        echo "$IP is not reachable."
    fi
done < "$IP_LIST"

echo "Results saved in $OUTPUT_FILE."
