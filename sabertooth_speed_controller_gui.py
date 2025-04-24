import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports

class SabertoothGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sabertooth Motor Controller GUI")

        # Serial connection
        self.serial_port = None
        self.port_var = tk.StringVar()

        # GUI layout
        self.create_widgets()

    def create_widgets(self):
        # COM Port selection
        ports = serial.tools.list_ports.comports()
        port_names = [port.device for port in ports]
        self.port_var.set(port_names[0] if port_names else "")

        ttk.Label(self.root, text="Serial Port:").grid(row=0, column=0, sticky="e")
        port_menu = ttk.Combobox(self.root, textvariable=self.port_var, values=port_names, state="readonly")
        port_menu.grid(row=0, column=1)
        ttk.Button(self.root, text="Connect", command=self.connect_serial).grid(row=0, column=2)

        # Motor 1
        ttk.Label(self.root, text="Motor 1").grid(row=1, column=0, columnspan=3)
        self.motor1_slider = tk.Scale(self.root, from_=-63, to=63, orient="horizontal", command=self.update_motor1)
        self.motor1_slider.grid(row=2, column=0, columnspan=3, sticky="ew")

        # Motor 2
        ttk.Label(self.root, text="Motor 2").grid(row=3, column=0, columnspan=3)
        self.motor2_slider = tk.Scale(self.root, from_=-63, to=63, orient="horizontal", command=self.update_motor2)
        self.motor2_slider.grid(row=4, column=0, columnspan=3, sticky="ew")

    def connect_serial(self):
        port = self.port_var.get()
        if self.serial_port:
            self.serial_port.close()
        try:
            self.serial_port = serial.Serial(port, 9600, timeout=1)
            print(f"Connected to {port}")
        except serial.SerialException:
            print(f"Failed to connect to {port}")

    def send_command(self, value):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(bytes([value]))
            print("Value: ", value)
            

    def update_motor1(self, val):
        speed = int(val)
        command = 64 + speed  # Valid range: 1–127
        command = max(1, min(127, command))
        self.send_command(command)
        print("Motor 1: ", command)

    def update_motor2(self, val):
        speed = int(val)
        command = 192 + speed  # Valid range: 128–255
        command = max(128, min(255, command))
        self.send_command(command)
        print("Motor 2: ", command)

if __name__ == "__main__":
    root = tk.Tk()
    app = SabertoothGUI(root)
    root.mainloop()
