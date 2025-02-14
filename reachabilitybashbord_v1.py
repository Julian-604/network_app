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

    while True:
        stdscr.clear()
        stdscr.addstr(0, 2, "Live Cisco Switch Monitoring", curses.A_BOLD)
        stdscr.addstr(1, 0, "=" * 80)
        stdscr.addstr(2, 2, "Name", curses.A_UNDERLINE)
        stdscr.addstr(2, 20, "IP Address", curses.A_UNDERLINE)
        stdscr.addstr(2, 40, "Status", curses.A_UNDERLINE)
        
        for i, switch in enumerate(switches):
            ip = switch["ip"]
            name = switch["name"]
            reachable = ping(ip)
            
            if not reachable:
                if ip not in last_down:
                    last_down[ip] = time.time()
                blink[ip] = (time.time() - last_down[ip]) < 30  # Blink for 30 seconds
                status[ip] = "DOWN"
            else:
                status[ip] = "UP"
                if ip in last_down:
                    del last_down[ip]
                if ip in blink:
                    del blink[ip]

            color = curses.color_pair(1) if status[ip] == "UP" else curses.color_pair(2)
            if blink.get(ip, False):
                color = curses.color_pair(3)

            row = 3 + (i % 25)  # Limit rows to fit in the terminal
            col = (i // 25) * 30  # Create columns dynamically
            stdscr.addstr(row, col + 2, name)
            stdscr.addstr(row, col + 20, ip)
            stdscr.addstr(row, col + 40, status[ip], color)
        
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
