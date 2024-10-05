import subprocess
import tkinter as tk
from tkinter import messagebox  # Add this import for messagebox
import os


def check_terminal():
    try:
        subprocess.run(["xfce4-terminal", "--version"], check=True)
        return True  # Terminal is installed
    except FileNotFoundError:
        # xfce4-terminal is not installed, so install it
        os.system("sudo apt update && sudo apt install -y xfce4-terminal")
        return False  # Terminal is not installed and was just installed

def show_info():
    selected_command = command_listbox.get(tk.ACTIVE)
    info_text = ""
    
    if selected_command == "checker":
        info_text = """
        Checker Command Information:
        - Example:
            BSSID:00:11:22:33:44:55
            Channel: 6
            Interface: wlan0mon
            File Name: output.cap
        """
    elif selected_command == "deauth":
        info_text = """
        Deauthentication Attack
        +It Sends Deauth Packets+
        Packets: 0 for unli 
        MainBssid: the main bssid you get from dump
        ClientBssid: the client bssid you get from checker
        Interface: wlan0mon
        """
    elif selected_command == "create ap":
        info_text = """
        Creation Of Access Points
        +it creates access points(basically wifi)+
        Name : whatever you want to name the network
        Channel : can put 1 - 17
        Interface: wlan0mon
        """
    elif selected_command == "dump bssid":
        info_text = """
        Dumps bssid to a file 
        +its dump but it just dumps to a file+
        bssid: its like dump 
        Interface: wlan0mon
        Channel: 1 - 17
        Filename : lol.pcap
        """
       
    elif selected_command == "crack":
        info_text = """
        Wifi Cracker
        +It Cracks the wifi .cap file with a pswd list+
        password:any .txt .lst
        """
        
    elif selected_command == "turn off":
        info_text = """
        Turn Off Command
        +it turns off airmon aka aircrack+
        Interface: wlan0mon
        """
        
    elif selected_command == "turn on":
        info_text = """
        Turn On Commnd
        +It turns on airmon for aircrack+
        Interface: wlan0
        """
    elif selected_command == "turn onV2":
        info_text = """
        Turn OnV2 Commnd
        +It turns on airmon for aircrack but its only used if you have 2 adapters+
        Interface: custom
        """
        
    elif selected_command == "dump":
        info_text = """
        Dump Command
        +It Dumps aps Bssid (wifis)+
        Interface: custom
        """
    if info_text:
        tk.messagebox.showinfo("Command Information", info_text)


def execute_selected():
    selected_command = command_listbox.get(tk.ACTIVE)
    
    if selected_command == "checker":
        bssid = bssid_entry.get()
        channel = channel_entry.get()
        inte = interface_entry.get()
        filename = filename_entry.get()
        command = f"sudo airodump-ng --bssid {bssid} --channel {channel} --write {filename} {inte}"
    elif selected_command == "deauth":
        packets = packets_entry.get()
        mainmac = mainmac_entry.get()
        clientmac = clientmac_entry.get()
        inte2 = interface2_entry.get()
        command = f"sudo aireplay-ng --deauth {packets} -a {mainmac} -c {clientmac} {inte2}"    
    elif selected_command == "dump":
        inte3 = interface3_entry.get()
        command = f"sudo airodump-ng {inte3}"
    elif selected_command == "crack":
        nig3 = nig3_entry.get()
        passfile = passfile_entry.get()
        command = f"sudo aircrack-ng {nig3} -w {passfile}"
    elif selected_command == "dump bssid":
        bssidd = bssidd_entry.get()
        inte7 = inte7_entry.get()
        channel123 = channel123_entry.get()
        filesave = filesave_entry.get()
        command = f"sudo airodump-ng -c {channel123} --bssid {bssidd} -w {filesave}.pcap {inte7}"
    elif selected_command == "create ap":
        name = name_entry.get()
        channel2 = channel2_entry.get()
        inte4 = inte4_entry.get()
        command = f"sudo airbase-ng -e {name} -c {channel2} {inte4}"
    elif selected_command == "turn off":
        inte5 = inte5_entry.get()
        command = f"sudo airmon-ng stop {inte5}"
        os.system("systemctl start NetworkManager")
    elif selected_command == "turn on":
        os.system("sudo airmon-ng check kill")
        command = "sudo airmon-ng start wlan0"
    elif selected_command == "turn onV2":
        hacker = hacker_entry.get()
        os.system("sudo airmon-ng check kill")
        command = f"sudo airmon-ng start {hacker}"
        os.system("systemctl start NetworkManager")
    elif selected_command == "guide":
         print("these are just basic but why not shit lmao\n")
         print("ap - Access points provides internet access in public places(aka its wifi)\n(the main file is ")
         
        
    subprocess.Popen(["xfce4-terminal", "--command", command])

def toggle_widgets():
    selected_command = command_listbox.get(tk.ACTIVE)
    
    for widget in all_widgets:
        widget.pack_forget()

    if selected_command == "checker":
        bssid_label.pack()
        bssid_entry.pack()
        channel_label.pack()
        channel_entry.pack()
        interface_label.pack()
        interface_entry.pack()
        filename_label.pack()
        filename_entry.pack()
    elif selected_command == "deauth":
        packets_label.pack()
        packets_entry.pack()
        mainmac_label.pack()
        mainmac_entry.pack()
        clientmac_label.pack()
        clientmac_entry.pack()
        interface2_label.pack()
        interface2_entry.pack()
    elif selected_command == "dump":
        interface3_label.pack()
        interface3_entry.pack()
    elif selected_command == "crack":
        nig3_label.pack()
        nig3_entry.pack()
        passfile_label.pack()
        passfile_entry.pack()
    elif selected_command == "dump bssid":
        bssidd_label.pack()
        bssidd_entry.pack()
        inte7_label.pack()
        inte7_entry.pack()
        channel123_label.pack()
        channel123_entry.pack()
        filesave_label.pack()
        filesave_entry.pack()
    elif selected_command == "create ap":
        name_label.pack()
        name_entry.pack()
        channel2_label.pack()
        channel2_entry.pack()
        inte4_label.pack()
        inte4_entry.pack()
    elif selected_command in ["turn off", "turn on"]:
        inte5_label.pack()
        inte5_entry.pack()
    elif selected_command == "turn onV2":
        hacker_label.pack()
        hacker_entry.pack()

root = tk.Tk()
root.title(" Bettercap Gui by letchu v1")

commands = ["checker", "deauth", "dump", "create ap", "dump bssid", "crack", "turn off", "turn on","turn onV2"]

command_frame = tk.Frame(root)
command_frame.pack()

command_label = tk.Label(command_frame, text="Select a command:")
command_label.pack()

command_listbox = tk.Listbox(command_frame, height=len(commands))
for command in commands:
    command_listbox.insert(tk.END, command)
command_listbox.pack(side=tk.LEFT)

info_button = tk.Button(command_frame, text="Information", command=show_info)
info_button.pack(side=tk.LEFT)

select_button = tk.Button(command_frame, text="Select", command=toggle_widgets)
select_button.pack(side=tk.LEFT)

# Initialize the terminal check
terminal_installed = check_terminal()

bssid_label = tk.Label(root, text="BSSID:")
bssid_entry = tk.Entry(root)

channel_label = tk.Label(root, text="Channel:")
channel_entry = tk.Entry(root)

interface_label = tk.Label(root, text="Interface:")
interface_entry = tk.Entry(root)

filename_label = tk.Label(root, text="File Name:")
filename_entry = tk.Entry(root)

packets_label = tk.Label(root, text="Packets:")
packets_entry = tk.Entry(root)

mainmac_label = tk.Label(root, text="Main MAC:")
mainmac_entry = tk.Entry(root)

clientmac_label = tk.Label(root, text="Client MAC:")
clientmac_entry = tk.Entry(root)

interface2_label = tk.Label(root, text="Interface:")
interface2_entry = tk.Entry(root)

interface3_label = tk.Label(root, text="Interface:")
interface3_entry = tk.Entry(root)

nig3_label = tk.Label(root, text=".cap file:")
nig3_entry = tk.Entry(root)

passfile_label = tk.Label(root, text="Password list:")
passfile_entry = tk.Entry(root)

bssidd_label = tk.Label(root, text="BSSID:")
bssidd_entry = tk.Entry(root)

inte7_label = tk.Label(root, text="Interface:")
inte7_entry = tk.Entry(root)

channel123_label = tk.Label(root, text="Channel:")
channel123_entry = tk.Entry(root)

filesave_label = tk.Label(root, text="File Name:")
filesave_entry = tk.Entry(root)

name_label = tk.Label(root, text="Name of the network:")
name_entry = tk.Entry(root)

channel2_label = tk.Label(root, text="Channel:")
channel2_entry = tk.Entry(root)

inte4_label = tk.Label(root, text="Interface:")
inte4_entry = tk.Entry(root)

inte5_label = tk.Label(root, text="Interface:")
inte5_entry = tk.Entry(root)

hacker_label = tk.Label(root, text="Interface:")
hacker_entry = tk.Entry(root)

all_widgets = [
    bssid_label, bssid_entry, channel_label, channel_entry, interface_label, interface_entry,
    filename_label, filename_entry, packets_label, packets_entry, mainmac_label, mainmac_entry,
    clientmac_label, clientmac_entry, interface2_label, interface2_entry, interface3_label,
    interface3_entry, nig3_label, nig3_entry, passfile_label, passfile_entry, bssidd_label,
    bssidd_entry, inte7_label, inte7_entry, channel123_label, channel123_entry, filesave_label,
    filesave_entry, name_label, name_entry, channel2_label, channel2_entry, inte4_label,
    inte4_entry, inte5_label, inte5_entry, hacker_label,hacker_entry
]

execute_button = tk.Button(root, text="Execute", command=execute_selected)
execute_button.pack()

window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

root.mainloop()
