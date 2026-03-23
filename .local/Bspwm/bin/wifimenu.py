#!/usr/bin/env python3
import subprocess
import sys
import time

# --- Configuration ---
WIFI_IFACE = "wlp2s0"
ETH_IFACE = "enp1s0f1"
ROFI_CMD = ["rofi", "-dmenu", "-i", "-selected-row", "0"]
CONN_TIMEOUT = 10

# --- Icons (Nerd Fonts) ---
ICONS = {
    "active": "󰖩",
    "saved": "",
    "secure": "",
    "eth_on": "󰈁",
    "eth_off": "󰈂",
    "reconnect": "󰑐",
    "disconnect": "󰅖"
}

def run(cmd):
    """Executes a command and returns the stripped output."""
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

def notify(title, message, urgency="normal"):
    """Sends a system notification."""
    icon = "network-transmit-receive" if urgency == "normal" else "network-error"
    subprocess.run(["notify-send", title, message, "-u", urgency, "-i", icon])

def get_eth_icon():
    """Checks Ethernet connection status."""
    state = run(f"nmcli -t -f DEVICE,STATE dev | grep '^{ETH_IFACE}:' | cut -d: -f2")
    return ICONS["eth_on"] if state == "connected" else ICONS["eth_off"]

def get_wifi_data():
    """Gathers Wi-Fi data using nmcli."""
    # Current active SSID
    current = run(f"nmcli -t -f NAME,DEVICE connection show --active | grep ':{WIFI_IFACE}$' | cut -d: -f1")
    
    # List of saved connections
    saved_raw = run("nmcli -t -f NAME,TYPE connection show")
    saved = [line.split(':')[0] for line in saved_raw.splitlines() if "802-11-wireless" in line]
    
    # List of available networks in range
    available_raw = run(f"nmcli -t -f 'SECURITY,SSID' device wifi list ifname {WIFI_IFACE}")
    available = []
    for line in available_raw.splitlines():
        if line.startswith('--') or not line.strip():
            continue
        parts = line.split(':')
        if len(parts) >= 2:
            available.append({'security': parts[0], 'ssid': parts[1]})
            
    return current, saved, available

def rofi(options, prompt):
    """Triggers Rofi menu and returns selection."""
    process = subprocess.Popen(ROFI_CMD + ["-p", prompt], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate(input="\n".join(options))
    return stdout.strip()

def main():
    # Ensure NetworkManager is running
    if subprocess.run(["systemctl", "is-active", "--quiet", "NetworkManager"]).returncode != 0:
        run("pkexec systemctl start NetworkManager")

    current_ssid, saved_ssids, available_nets = get_wifi_data()
    eth_icon = get_eth_icon()
    
    menu = []
    processed = set()

    # 1. Active Network
    if current_ssid:
        menu.append(f"{ICONS['active']}  {current_ssid} (Active)")
        processed.add(current_ssid)

    # 2. Saved Networks
    for ssid in saved_ssids:
        if ssid and ssid not in processed:
            menu.append(f"{ICONS['saved']}  {ssid}")
            processed.add(ssid)

    # 3. Available Networks in Air
    for net in available_nets:
        ssid = net['ssid']
        if ssid and ssid not in processed:
            icon = ICONS['secure'] if "WPA" in net['security'] else ICONS['saved']
            menu.append(f"{icon}  {ssid}")
            processed.add(ssid)

    chosen = rofi(menu, f"({eth_icon}) Wi-Fi:")
    if not chosen:
        sys.exit(0)

    # Extract clean SSID from the chosen string
    clean_ssid = chosen
    for icon in ICONS.values():
        clean_ssid = clean_ssid.replace(icon, "")
    clean_ssid = clean_ssid.replace("(Active)", "").strip()

    # --- Active Network Submenu ---
    if "(Active)" in chosen:
        action = rofi([f"{ICONS['reconnect']} Reconnect", f"{ICONS['disconnect']} Disconnect"], f"Action for {clean_ssid}:")
        if "Reconnect" in action:
            notify("Wi-Fi", f"Reconnecting to {clean_ssid}...")
            run(f"nmcli device disconnect {WIFI_IFACE}")
            time.sleep(1)
            run(f"nmcli --wait {CONN_TIMEOUT} connection up id '{clean_ssid}'")
        elif "Disconnect" in action:
            run(f"nmcli device disconnect {WIFI_IFACE}")
            notify("Wi-Fi", f"Disconnected from {clean_ssid}")
        sys.exit(0)

    # --- Connection Logic with Range Validation ---
    
    # Check if the chosen network is actually visible in the air
    is_in_range = any(net['ssid'] == clean_ssid for net in available_nets)
    
    if not is_in_range:
        notify("Error", f"Network '{clean_ssid}' is not in range", urgency="critical")
        sys.exit(1)

    notify("Wi-Fi", f"Connecting to {clean_ssid}...")
    
    if clean_ssid in saved_ssids:
        # Connect to existing profile
        cmd = f"nmcli --wait {CONN_TIMEOUT} connection up id '{clean_ssid}'"
    else:
        # Connect to new network (with password if secure)
        if ICONS['secure'] in chosen:
            password = rofi([], f"Password for {clean_ssid}:")
            if not password:
                sys.exit(0)
            cmd = f"nmcli --wait {CONN_TIMEOUT} device wifi connect '{clean_ssid}' password '{password}'"
        else:
            cmd = f"nmcli --wait {CONN_TIMEOUT} device wifi connect '{clean_ssid}'"

    run(cmd)
    
    # Final Verification
    time.sleep(2)
    check = run(f"nmcli -t -f NAME,DEVICE connection show --active | grep ':{WIFI_IFACE}$' | cut -d: -f1")
    if check == clean_ssid:
        notify("Wi-Fi", f"Connected to {clean_ssid}")
    else:
        notify("Error", f"Connection to {clean_ssid} failed", urgency="critical")

if __name__ == "__main__":
    main()
