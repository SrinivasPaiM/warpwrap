import os
import subprocess
import webbrowser
import psutil
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


def is_warp_installed():
    """Check if warp-cli is installed by trying to get its version."""
    try:
        subprocess.run(["warp-cli", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def offer_warp_install():
    """Open Cloudflare WARP install page"""
    response = CTkMessagebox(
        title="WARP Not Found",
        message="Cloudflare WARP is not installed. Do you want to open the download page?",
        icon="question",
        option_1="Yes",
        option_2="No"
    )
    if response.get() == "Yes":
        webbrowser.open("https://1.1.1.1/")


def enable_warp():
    """Enable WARP using the WARP CLI"""
    if not is_warp_installed():
        offer_warp_install()
        return
    try:
        subprocess.run(["warp-cli", "connect"], check=True)
        update_status_display(True)
        CTkMessagebox(title="Success", message="WARP is enabled!", icon="check")
    except subprocess.CalledProcessError:
        CTkMessagebox(title="Error", message="Failed to enable WARP.", icon="cancel")


def disable_warp():
    """Disable WARP using the WARP CLI"""
    if not is_warp_installed():
        offer_warp_install()
        return
    try:
        subprocess.run(["warp-cli", "disconnect"], check=True)
        update_status_display(False)
        CTkMessagebox(title="Success", message="WARP is disabled!", icon="check")
    except subprocess.CalledProcessError:
        CTkMessagebox(title="Error", message="Failed to disable WARP.", icon="cancel")


def check_warp_status():
    """Check WARP connection status and update the UI"""
    if not is_warp_installed():
        offer_warp_install()
        return
    try:
        result = subprocess.run(["warp-cli", "status"], capture_output=True, text=True)
        is_connected = "Connected" in result.stdout
        update_status_display(is_connected)

        status_msg = "WARP is currently active." if is_connected else "WARP is not active."
        CTkMessagebox(title="WARP Status", message=status_msg, icon="info")
    except subprocess.CalledProcessError:
        CTkMessagebox(title="Error", message="Failed to check WARP status.", icon="cancel")


def update_status_display(is_connected):
    """Update the status display in the UI"""
    if is_connected:
        status_label.configure(text="WARP Status: Connected", text_color="#00aa00")
        status_indicator.configure(fg_color="#00aa00")
    else:
        status_label.configure(text="WARP Status: Disconnected", text_color="#aa0000")
        status_indicator.configure(fg_color="#aa0000")


def open_dns_leak_test():
    """Open the DNS leak test website"""
    webbrowser.open("https://www.dnsleaktest.com/")


def check_steam_process():
    """Check if Steam is running and notify the user"""
    for proc in psutil.process_iter(["name"]):
        try:
            if "steam" in proc.info["name"].lower():
                CTkMessagebox(
                    title="Steam Detected",
                    message="Steam is running. Consider enabling WARP or a Proxy.",
                    icon="warning"
                )
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    CTkMessagebox(title="Steam Status", message="Steam is not currently running.", icon="info")


def check_epic_process():
    """Check if Epic Games Launcher is running"""
    for proc in psutil.process_iter(["name"]):
        try:
            if "epicgameslauncher" in proc.info["name"].lower():
                CTkMessagebox(title="Epic Games Detected", message="Epic Games Launcher is running.", icon="info")
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    CTkMessagebox(title="Epic Games Status", message="Epic Games is not currently running.", icon="info")


def disable_warp_buttons():
    """Disable all WARP-related buttons if warp-cli is not installed"""
    for btn in warp_buttons:
        btn.configure(state="disabled")


def check_and_warn_warp():
    """Check at startup and warn user if WARP CLI is not installed"""
    if not is_warp_installed():
        disable_warp_buttons()
        response = CTkMessagebox(
            title="WARP CLI Required",
            message="Cloudflare WARP CLI is not installed.\n\nThis app needs 'warp-cli' to work.\nDo you want to open the download page?",
            icon="warning",
            option_1="Yes",
            option_2="No"
        )
        if response.get() == "Yes":
            webbrowser.open("https://1.1.1.1/")


def toggle_warp(event=None):
    """Toggle WARP state on Ctrl+Shift+Q"""
    if not is_warp_installed():
        offer_warp_install()
        return
    result = subprocess.run(["warp-cli", "status"], capture_output=True, text=True)
    if "Connected" in result.stdout:
        disable_warp()
    else:
        enable_warp()


def apply_theme(new_mode):
    """Apply the selected theme mode"""
    ctk.set_appearance_mode(new_mode)


# --- GUI Setup ---
root = ctk.CTk()
root.title("Cloudflare WARP Manager")
root.geometry("480x580")
root.resizable(False, False)

# Create a main frame with padding
main_frame = ctk.CTkFrame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Main header
header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
header_frame.pack(fill="x", pady=10)

header_label = ctk.CTkLabel(header_frame, text="Cloudflare WARP Manager", font=ctk.CTkFont(size=22, weight="bold"))
header_label.pack(side="left", padx=10)

# Status display area
status_frame = ctk.CTkFrame(main_frame)
status_frame.pack(fill="x", pady=15)

status_indicator = ctk.CTkLabel(status_frame, text="", width=20, height=20, fg_color="#aa0000", corner_radius=10)
status_indicator.pack(side="left", padx=15)

status_label = ctk.CTkLabel(status_frame, text="WARP Status: Disconnected", font=ctk.CTkFont(size=14),
                            text_color="#aa0000")
status_label.pack(side="left")

# WARP Controls Frame
warp_frame = ctk.CTkFrame(main_frame)
warp_frame.pack(fill="x", pady=10)

warp_frame_header = ctk.CTkLabel(warp_frame, text="WARP Controls", font=ctk.CTkFont(size=16, weight="bold"))
warp_frame_header.pack(pady=10)

warp_buttons = []

btn_enable = ctk.CTkButton(
    warp_frame,
    text="Enable WARP",
    command=enable_warp,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=14)
)
btn_enable.pack(padx=20, pady=10, fill="x")
warp_buttons.append(btn_enable)

btn_disable = ctk.CTkButton(
    warp_frame,
    text="Disable WARP",
    command=disable_warp,
    height=40,
    corner_radius=8,
    fg_color="#aa5555",
    hover_color="#aa3333",
    font=ctk.CTkFont(size=14)
)
btn_disable.pack(padx=20, pady=10, fill="x")
warp_buttons.append(btn_disable)

btn_status = ctk.CTkButton(
    warp_frame,
    text="Check WARP Status",
    command=check_warp_status,
    height=40,
    corner_radius=8,
    fg_color="#555555",
    hover_color="#333333",
    font=ctk.CTkFont(size=14)
)
btn_status.pack(padx=20, pady=10, fill="x")
warp_buttons.append(btn_status)

# Network Tools Frame
nettools_frame = ctk.CTkFrame(main_frame)
nettools_frame.pack(fill="x", pady=10)

nettools_header = ctk.CTkLabel(nettools_frame, text="Network Tools", font=ctk.CTkFont(size=16, weight="bold"))
nettools_header.pack(pady=10)

btn_steam = ctk.CTkButton(
    nettools_frame,
    text="Check if Steam is Running",
    command=check_steam_process,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=14)
)
btn_steam.pack(padx=20, pady=10, fill="x")

btn_epic = ctk.CTkButton(
    nettools_frame,
    text="Check if Epic Games is Running",
    command=check_epic_process,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=14)
)
btn_epic.pack(padx=20, pady=10, fill="x")

btn_dns = ctk.CTkButton(
    nettools_frame,
    text="Open DNS Leak Test",
    command=open_dns_leak_test,
    height=40,
    corner_radius=8,
    font=ctk.CTkFont(size=14)
)
btn_dns.pack(padx=20, pady=10, fill="x")

# Settings frame
settings_frame = ctk.CTkFrame(main_frame)
settings_frame.pack(fill="x", pady=10)

settings_header = ctk.CTkLabel(settings_frame, text="Settings", font=ctk.CTkFont(size=16, weight="bold"))
settings_header.pack(pady=10)

# Theme selection
theme_var = ctk.StringVar(value="System")
theme_label = ctk.CTkLabel(settings_frame, text="Theme Mode:")
theme_label.pack(padx=20, anchor="w")

theme_combobox = ctk.CTkComboBox(
    settings_frame,
    values=["System", "Light", "Dark"],
    command=apply_theme,
    variable=theme_var,
    width=200
)
theme_combobox.pack(padx=20, pady=5, anchor="w")

# Footer Label
footer = ctk.CTkLabel(
    main_frame,
    text="By Srinivas - Modern Windows Edition",
    font=ctk.CTkFont(size=12),
    text_color="gray"
)
footer.pack(pady=15)

# Keyboard shortcut info
shortcut_label = ctk.CTkLabel(
    main_frame,
    text="Press Ctrl+Shift+Q to toggle WARP",
    font=ctk.CTkFont(size=11),
    text_color="gray"
)
shortcut_label.pack()

# Bind the shortcut (Ctrl+Shift+Q) to toggle WARP
root.bind('<Control-Shift-Q>', toggle_warp)

# Initial check for warp-cli and WARP status
check_and_warn_warp()
if is_warp_installed():
    try:
        result = subprocess.run(["warp-cli", "status"], capture_output=True, text=True)
        update_status_display("Connected" in result.stdout)
    except:
        pass

# Run the GUI event loop
root.mainloop()
