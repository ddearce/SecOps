import os
import socket
import csv
import uuid
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, simpledialog
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import nmap

# Variables globales para la configuración
auto_scan_interval = 0  # Intervalo de escaneo automático en segundos
last_scan_time = None   # Último tiempo de escaneo
auto_scan_thread = None  # Hilo para el escaneo automático
scanned_ips = 0  # Variable global para llevar un seguimiento de las IPs escaneadas

def get_device_info(ip):
    try:
        host_info = socket.gethostbyaddr(ip)
        mac_address = ':'.join(['{:02x}'.format(b) for b in uuid.UUID(int=uuid.getnode()).bytes[-6:]])
        return {
            'IP Address': ip,
            'Hostname': host_info[0],
            'MAC Address': mac_address
        }
    except (socket.herror, socket.gaierror):
        return None

def scan_ports(ip):
    open_ports = []
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=ip, arguments='-F')  # Scan common ports
        for host in nm.all_hosts():
            if 'tcp' in nm[host]:
                open_ports.extend(nm[host]['tcp'].keys())
        return open_ports
    except nmap.PortScannerError:
        return None

def is_host_alive(ip):
    # Realizar un ping al host para verificar si está activo
    try:
        response = os.system(f"ping -n 1 -w 1 {ip}")  # Windows
        return response == 0
    except Exception:
        return False

def scan_network(ip_range, progress_bar, progress_label):
    devices = []
    total_ips = 254  # Total de IPs en el rango
    global scanned_ips  # Declarar scanned_ips como global

    with ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(1, 255):
            ip = f"{ip_range}.{i}"
            if is_host_alive(ip):
                future = executor.submit(get_device_info, ip)
                devices.append({'IP Address': ip})  # Agregar el dispositivo incluso si no se puede obtener más información
                future.add_done_callback(lambda future, ip=ip: update_scan_progress(future, ip, devices, progress_bar, progress_label, total_ips))
    
    return devices

def update_scan_progress(future, ip, devices, progress_bar, progress_label, total_ips):
    device_info = future.result()
    if device_info:
        open_ports = scan_ports(ip)
        if open_ports is not None:
            device_info['Open Ports'] = ', '.join(map(str, open_ports))
        # Buscar el dispositivo por dirección IP en la lista y actualizar la información
        for device in devices:
            if device['IP Address'] == ip:
                device.update(device_info)
        
        global scanned_ips  # Declarar scanned_ips como global
        scanned_ips += 1
        progress_bar["value"] = (scanned_ips / total_ips) * 100
        progress_label.config(text=f"Scanning {ip}... ({scanned_ips}/{total_ips})")

def generate_report(devices, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['IP Address', 'Hostname', 'MAC Address', 'Open Ports'])
        writer.writeheader()
        writer.writerows(devices)

def browse_output_path(output_path_entry):
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    output_path_entry.delete(0, tk.END)
    output_path_entry.insert(0, output_path)

def auto_scan_loop(ip_range_entry, output_path_entry, progress_bar, progress_label):
    global auto_scan_interval, auto_scan_thread
    while True:
        start_scan(ip_range_entry, output_path_entry, progress_bar, progress_label)
        time.sleep(auto_scan_interval)

def start_scan(ip_range_entry, output_path_entry, progress_bar, progress_label):
    global last_scan_time, auto_scan_thread
    ip_range = ip_range_entry.get()
    output_path = output_path_entry.get()
    
    # Siempre permite el escaneo manual
    if auto_scan_interval > 0 and (last_scan_time is None or time.time() - last_scan_time >= auto_scan_interval):
        last_scan_time = time.time()
        if auto_scan_thread is None or not auto_scan_thread.is_alive():
            auto_scan_thread = threading.Thread(target=scan_network_thread, args=(ip_range, output_path, progress_bar, progress_label))
            auto_scan_thread.start()
    else:
        # Muestra un mensaje solo si se intenta realizar un escaneo automático manualmente
        if auto_scan_interval > 0:
            messagebox.showinfo("Info", "Auto-scan is not scheduled now.")
        else:
            # Ejecuta el escaneo manual en un hilo separado
            manual_scan_thread = threading.Thread(target=scan_network_thread, args=(ip_range, output_path, progress_bar, progress_label))
            manual_scan_thread.start()
            


def scan_network_thread(ip_range, output_path, progress_bar, progress_label):
    devices = scan_network(ip_range, progress_bar, progress_label)
    generate_report(devices, output_path)  # Generar informe incluso si no hay dispositivos
    if devices:
        progress_label.config(text=f"Inventory report saved to {output_path}")
    else:
        progress_label.config(text="No active devices found in the network.")

    progress_bar["value"] = 100  # Asegúrate de que la barra de progreso llegue al 100%
    progress_label.config(text="Scan completed")  # Indica que el escaneo ha finalizado

def configure_auto_scan():
    global auto_scan_interval  # Usar la variable global auto_scan_interval
    auto_scan_interval = simpledialog.askinteger("Auto Scan Interval", "Enter the scan interval in seconds (0 to disable):")
    if auto_scan_interval is not None:
        messagebox.showinfo("Info", f"Auto-scan interval set to {auto_scan_interval} seconds.")
    else:
        messagebox.showinfo("Info", "Auto-scan is disabled.")

root = tk.Tk()
root.title("SecOps Network Inventory Tool (SONIT)")
root.geometry("400x300")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

label = ttk.Label(frame, text="Enter the first three octets of the IP range:")
label.pack()

ip_range_entry = ttk.Entry(frame)
ip_range_entry.pack()

output_path_label = ttk.Label(frame, text="Choose where to save the report:")
output_path_label.pack()

output_path_entry = ttk.Entry(frame)
output_path_entry.pack()

browse_button = ttk.Button(frame, text="Browse", command=lambda: browse_output_path(output_path_entry))
browse_button.pack()

start_button = ttk.Button(frame, text="Start Scan", command=lambda: start_scan(ip_range_entry, output_path_entry, progress_bar, progress_label))
start_button.pack()

auto_scan_interval = 0

auto_scan_button = ttk.Button(frame, text="Configure Auto Scan", command=configure_auto_scan)
auto_scan_button.pack()

scan_button = ttk.Button(frame, text="Run Auto Scan", command=lambda: threading.Thread(target=auto_scan_loop, args=(ip_range_entry, output_path_entry, progress_bar, progress_label)).start())
scan_button.pack()

progress_label = ttk.Label(frame, text="")
progress_label.pack()

progress_bar = ttk.Progressbar(frame, length=300, mode="determinate")
progress_bar.pack()

root.mainloop()
