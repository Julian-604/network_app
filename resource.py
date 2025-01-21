import shutil
import psutil
import logging

def check_disk_usage(threshold):
    """
    Checks disk usage for the root filesystem and returns True if the usage exceeds the threshold.
    """
    total, used, free = shutil.disk_usage("/")
    percent_used = (used / total) * 100
    return percent_used, percent_used > threshold

def check_ram_usage(threshold):
    """
    Checks RAM usage and returns True if the usage exceeds the threshold.
    """
    memory = psutil.virtual_memory()
    percent_used = memory.percent
    return percent_used, percent_used > threshold

def check_network_speed():
    """
    Checks network bandwidth usage.
    Returns bytes sent and received per second.
    """
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def log_alert(message):
    """
    Logs an alert message to a log file.
    """
    logging.basicConfig(
        filename="system_alerts.log",
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.warning(message)

def main():
    # Configuration
    DISK_THRESHOLD = 80  # Set disk usage threshold in percentage
    RAM_THRESHOLD = 80   # Set RAM usage threshold in percentage

    # Check disk usage
    disk_percent_used, is_disk_exceeded = check_disk_usage(DISK_THRESHOLD)

    if is_disk_exceeded:
        message = (
            f"Warning! Disk usage has exceeded the threshold of {DISK_THRESHOLD}% on the root filesystem.\n"
            f"Current Usage: {disk_percent_used:.2f}%\n"
            f"Please take necessary actions to free up space."
        )
        log_alert(message)
        print("Disk usage alert logged.")
    else:
        print(f"Disk usage is within limits: {disk_percent_used:.2f}% used.")

    # Check RAM usage
    ram_percent_used, is_ram_exceeded = check_ram_usage(RAM_THRESHOLD)

    if is_ram_exceeded:
        message = (
            f"Warning! RAM usage has exceeded the threshold of {RAM_THRESHOLD}%.\n"
            f"Current Usage: {ram_percent_used:.2f}%\n"
            f"Please take necessary actions to optimize memory usage."
        )
        log_alert(message)
        print("RAM usage alert logged.")
    else:
        print(f"RAM usage is within limits: {ram_percent_used:.2f}% used.")

    # Check network speed
    bytes_sent, bytes_recv = check_network_speed()
    print(f"Network usage: {bytes_sent / 1024:.2f} KB sent, {bytes_recv / 1024:.2f} KB received.")

if __name__ == "__main__":
    main()
