import curses
import time
import subprocess

# Load switches from a text file
def load_switches(file_path):
    switches = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                switches.append({"ip": parts[0], "name": parts[1]})
    return switches

switches = load_switches("switches.txt")

def ping(ip):
    """Ping the given IP address and return True if reachable, False otherwise."""
    result = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def display(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(1000)  # Refresh every second
    status = {}
    last_down = {}
    blink = {}
    down_time = {}

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Live Cisco Switch Monitoring", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 80)
        stdscr.addstr(2, 2, "Reachable Devices", curses.A_UNDERLINE)
        stdscr.addstr(2, 40, "Unreachable Devices", curses.A_UNDERLINE)
        
        up_row = 3
        down_row = 3
        
        for switch in switches:
            ip = switch["ip"]
            name = switch["name"]
            reachable = ping(ip)
            
            if not reachable:
                if ip not in last_down:
                    last_down[ip] = time.time()
                blink[ip] = (time.time() - last_down[ip]) < 30  # Blink for 30 seconds
                status[ip] = "DOWN"
                down_time[ip] = time.strftime('%H:%M:%S', time.localtime(last_down[ip]))
            else:
                status[ip] = "UP"
                if ip in last_down:
                    del last_down[ip]
                if ip in blink:
                    del blink[ip]
                if ip in down_time:
                    del down_time[ip]

            color = curses.color_pair(1) if status[ip] == "UP" else curses.color_pair(2)
            if blink.get(ip, False):
                color = curses.color_pair(3)
            
            if status[ip] == "UP":
                stdscr.addstr(up_row, 2, f"{name} ({ip})", color)
                up_row += 1
            else:
                stdscr.addstr(down_row, 40, f"{name} ({ip}) - Down Since: {down_time[ip]}", color)
                down_row += 1
        
        stdscr.refresh()
        if stdscr.getch() == ord('q'):
            break

def main():
    curses.wrapper(lambda stdscr: setup_colors(stdscr) or display(stdscr))

def setup_colors(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # UP - Green
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # DOWN - Red
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Blinking DOWN

if __name__ == "__main__":
    main()
