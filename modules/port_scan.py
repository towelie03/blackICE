import socket
from datetime import datetime
from threading import Thread, Lock

from core.logger import log_info, log_error

COMMON_PORTS = {
    20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
    53: "dns", 80: "http", 110: "pop3", 139: "netbios-ssn", 143: "imap",
    443: "https", 445: "microsoft-ds", 3389: "ms-wbt-server",
    3306: "mysql", 1433: "mssql", 1521: "oracle-db", 5900: "vnc",
    8080: "http-proxy"
}

open_ports = []
lock = Lock()

# ---------------------- BANNER GRABBING ----------------------

def grab_rdp_version(target, port=3389):
    """
    Minimal RDP handshake to extract version (Milestone 1 level)
    """
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))
        # Minimal RDP negotiation request
        request = bytes.fromhex('030000130e0000000000000001000800')
        sock.sendall(request)
        response = sock.recv(1024)
        sock.close()
        if len(response) >= 14:
            version = f"RDP Version {response[11]}.{response[12]}"
            return version
        return "RDP unknown version"
    except Exception:
        return "RDP unknown version"

def grab_banner(target, port, service):
    """
    Grab banners/versions for common services
    """
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((target, port))

        # Service-specific probes
        if service in ["http", "https", "http-proxy"]:
            sock.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        elif service == "smtp":
            sock.sendall(b"EHLO example.com\r\n")
        elif service == "ms-wbt-server":
            return grab_rdp_version(target, port)
        # SSH, FTP, and others usually send banner automatically

        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner if banner else "unknown"
    except Exception:
        return "unknown"

# ---------------------- PORT SCAN FUNCTION ----------------------

def scan_port(target, port):
    """Threaded scan for a single port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        service = COMMON_PORTS.get(port, "unknown")
        if result == 0:
            banner = grab_banner(target, port, service)
            with lock:
                open_ports.append((port, service, banner))
        sock.close()
    except Exception as e:
        log_error(f"Error scanning port {port}: {e}")

# ---------------------- MAIN RUN FUNCTION ----------------------

def run(target):
    start_time = datetime.now()
    print(f"\nStarting BlackICE TCP Scan at {start_time}")
    print(f"Scan report for {target}")

    # Interactive port range
    port_input = input("Enter port range (e.g., 20-1024) or leave blank for common ports: ").strip()
    if port_input:
        try:
            start, end = map(int, port_input.split("-"))
            ports = list(range(start, end + 1))
        except Exception:
            log_error("Invalid input. Scanning common ports instead.")
            ports = list(COMMON_PORTS.keys())
    else:
        ports = list(COMMON_PORTS.keys())

    threads = []
    max_threads = 50  

    for port in ports:
        t = Thread(target=scan_port, args=(target, port))
        threads.append(t)
        t.start()
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []

    for thread in threads:
        thread.join()

    # ---------------------- DISPLAY RESULTS ----------------------
    print(f"\nHost is up")
    closed_count = len(ports) - len(open_ports)
    print(f"Not shown: {closed_count} closed tcp ports\n")

    if open_ports:
        print(f"{'PORT':<10}{'STATE':<10}{'SERVICE':<15}{'VERSION'}")
        for port, service, banner in sorted(open_ports):
            print(f"{str(port)}/tcp".ljust(10) + "open".ljust(10) + service.ljust(15) + banner)

    end_time = datetime.now()
    duration = end_time - start_time
    print(f"\nScan finished at {end_time} (Duration: {duration})")
    log_info(f"Scan finished on {target}")
    log_info(f"Open ports: {open_ports}")




