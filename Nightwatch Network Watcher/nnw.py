import tkinter as tk
from tkinter import scrolledtext, simpledialog
import threading
from scapy.all import ARP, Ether, srp
import yagmail
import json
from datetime import datetime, timedelta

# Configuración de la aplicación
app_title = "NightWatch Network Monitor - by Damian de Arce"
monitoring = False

# Rango de IP para monitorear (modifica según tus necesidades)
ip_range = "192.168.1.1/24"

# Configuración del servidor SMTP
smtp_username = None
smtp_password = None
sender_email = None
receiver_email = None

# Ventana de status
status_window = None

# Diccionario para llevar un registro de la última vez que se envió una alerta para cada host no permitido
last_alert_time = {}

# Diccionario para mantener un registro de los hosts vistos
hosts_seen = {}

# Tiempo de espera antes de enviar otra alerta (24 horas en segundos)
alert_interval = 24 * 60 * 60

# Función para agregar mensajes al status
def add_status_message(message):
    if status_window is not None:
        status_window.insert(tk.END, message + "\n")
        status_window.see(tk.END)

# Función para cargar la lista de hosts permitidos desde un archivo de texto
def load_allowed_hosts(filename):
    allowed_hosts = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    ip, mac = parts[0], parts[1]
                    allowed_hosts[ip] = mac
        return allowed_hosts
    except Exception as e:
        print(f"Error loading allowed hosts from file: {str(e)}")
        return {}

# Función para cargar la configuración desde el archivo de configuración
def load_config():
    try:
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            return config_data
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return {}

# Función para guardar la configuración en el archivo de configuración
def save_config(config_data):
    try:
        with open("config.json", "w") as config_file:
            json.dump(config_data, config_file, indent=4)
    except Exception as e:
        add_status_message(f"Error saving config: {str(e)}")

# Función para cargar la última subnet escaneada desde la configuración
def load_last_subnet():
    try:
        config_data = load_config()
        return config_data.get("last_subnet", "")
    except Exception as e:
        add_status_message(f"Error loading last subnet: {str(e)}")
        return ""

# Función para guardar la última subnet escaneada en la configuración
def save_last_subnet(subnet):
    try:
        config_data = load_config()
        config_data["last_subnet"] = subnet
        save_config(config_data)
    except Exception as e:
        add_status_message(f"Error saving last subnet: {str(e)}")

# Función para enviar correo electrónico
def send_email(subject, message):
    try:
        yag = yagmail.SMTP(smtp_username, smtp_password)
        yag.send(
            to=receiver_email,
            subject=subject,
            contents=message
        )
        yag.close()
        return True
    except Exception as e:
        add_status_message(f"Error sending email: {str(e)}")
        return False

# Nombre del archivo JSON para almacenar la última alerta para cada host no permitido
last_alert_filename = "last_alert.json"

# Función para cargar la última alerta para cada host no permitido
def load_last_alert_time():
    try:
        with open(last_alert_filename, "r") as last_alert_file:
            return json.load(last_alert_file)
    except Exception as e:
        add_status_message(f"Error loading last alert times: {str(e)}")
        return {}

# Función para guardar la última alerta para cada host no permitido
def save_last_alert_time():
    try:
        with open(last_alert_filename, "w") as last_alert_file:
            json.dump(last_alert_time, last_alert_file, indent=4)  # Agrega el argumento 'indent' para formato legible
    except Exception as e:
        add_status_message(f"Error saving last alert times: {str(e)}")

# Función para escanear la red
def scan_network(subnet):
    global monitoring
    monitoring = True
    while monitoring:
        try:
            add_status_message("Escaneando la red...")
            
            # Cargar la lista de hosts permitidos desde el archivo
            allowed_hosts = load_allowed_hosts(filename)
            
            # Envía un ARP request y obtén las respuestas
            arp = ARP(pdst=subnet)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            result = srp(packet, timeout=3, verbose=0)[0]

            # Procesa las respuestas y envía correos si se encuentra un host no permitido
            for sent, received in result:
                if received.psrc != sender_email:
                    host_info = f"Host IP: {received.psrc}\nHost MAC: {received.hwsrc}"
                    
                    # Comprueba si el host está permitido
                    if received.psrc in allowed_hosts:
                        if received.hwsrc != allowed_hosts[received.psrc]:
                            alert_message = f"ALERTA: Host con IP {received.psrc} tiene una MAC diferente: {received.hwsrc}\n"
                            host_info = alert_message + host_info
                            if send_email("Alerta de Host Detectado", host_info):
                                add_status_message(f"Email de alerta enviado para host: {received.psrc}")
                    else:
                        # Comprueba si ha pasado al menos 24 horas desde la última alerta para este host
                        now = datetime.now()
                        last_alert = last_alert_time.get(received.psrc)
                        if last_alert is None:
                            last_alert_datetime = datetime.min  # Inicializa con una fecha muy temprana
                        else:
                            last_alert_datetime = datetime.strptime(last_alert, '%Y-%m-%d %H:%M:%S')
                        
                        time_difference = now - last_alert_datetime

                        if time_difference >= timedelta(seconds=alert_interval):
                            alert_message = f"ALERTA: Host no permitido detectado con IP {received.psrc}, MAC: {received.hwsrc}\n"
                            host_info = alert_message + host_info
                            if send_email("Alerta de Host No Permitido Detectado", host_info):
                                add_status_message(f"Email de alerta enviado para host no permitido: {received.psrc}")
                                # Formatea la hora como una cadena antes de almacenarla
                                last_alert_time[received.psrc] = now.strftime('%Y-%m-%d %H:%M:%S')
                                # Registra el tiempo de la última vez que se vio el host
                                hosts_seen[received.psrc] = {
                                    "mac": received.hwsrc,
                                    "last_seen": now.strftime('%Y-%m-%d %H:%M:%S')
                                }
                        else:
                            add_status_message("Host no autorizado detectado, pero lo vi hace menos de 24 horas, ignorando envío de email")

        except Exception as e:
            add_status_message(f"Error scanning network: {str(e)}")

# Función para detener el monitoreo
def stop_monitoring():
    global monitoring
    monitoring = False
    start_stop_button.config(text="Iniciar", command=start_monitoring)
    start_stop_button.config(state=tk.NORMAL)

# Función para iniciar el monitoreo
def start_monitoring():
    global monitoring
    monitoring = True
    start_stop_button.config(text="Detener", command=stop_monitoring)
    start_stop_button.config(state=tk.NORMAL)
    subnet = subnet_entry.get()
    save_last_subnet(subnet)  # Guardar la última subnet ingresada
    scan_thread = threading.Thread(target=scan_network, args=(subnet,))
    scan_thread.daemon = True
    scan_thread.start()

# Función para configurar los ajustes del servidor de correo
def configure_email_settings():
    global smtp_username, smtp_password, sender_email, receiver_email
    smtp_username = simpledialog.askstring("Configuración de correo", "Nombre de usuario SMTP:")
    smtp_password = simpledialog.askstring("Configuración de correo", "Contraseña SMTP:")
    sender_email = simpledialog.askstring("Configuración de correo", "Correo electrónico del remitente:")
    receiver_email = simpledialog.askstring("Configuración de correo", "Correo electrónico del destinatario:")

    # Guardar los ajustes en un archivo de configuración
    config_data = {
        "smtp_username": smtp_username,
        "smtp_password": smtp_password,
        "sender_email": sender_email,
        "receiver_email": receiver_email
    }
    save_config(config_data)

# Función para guardar el registro de hosts vistos en un archivo JSON
def save_hosts_seen():
    try:
        with open("hosts_seen.json", "w") as hosts_seen_file:
            json.dump(hosts_seen, hosts_seen_file, indent=4)  # Agrega el argumento 'indent' para formato legible
    except Exception as e:
        add_status_message(f"Error saving hosts seen: {str(e)}")

# Función para cargar el registro de hosts vistos desde un archivo JSON
def load_hosts_seen():
    try:
        with open("hosts_seen.json", "r") as hosts_seen_file:
            return json.load(hosts_seen_file)
    except Exception as e:
        add_status_message(f"Error loading hosts seen: {str(e)}")
        return {}

# Nombre del archivo de texto que contiene la lista de hosts permitidos
filename = "allowed_hosts.txt"

# Cargar la configuración desde el archivo de configuración
config_data = load_config()
if config_data:
    smtp_username = config_data.get("smtp_username")
    smtp_password = config_data.get("smtp_password")
    sender_email = config_data.get("sender_email")
    receiver_email = config_data.get("receiver_email")

# Cargar el registro de hosts vistos desde el archivo al iniciar la aplicación
hosts_seen = load_hosts_seen()

# Crear ventana principal
window = tk.Tk()
window.title(app_title)

# Cargar la imagen de fondo
background_image = tk.PhotoImage(file="background.png")
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Crear un marco para organizar los elementos
frame = tk.Frame(window, bg="white", padx=20, pady=20)
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# Crear una etiqueta para la subred
subnet_label = tk.Label(frame, text="Subred a escanear:", bg="white")
subnet_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Crear un cuadro de entrada para ingresar la subred
subnet_entry = tk.Entry(frame)
subnet_entry.grid(row=0, column=1, padx=10, pady=10)

# Crear botón "Ajustes" o "Configuración"
config_button = tk.Button(frame, text="Ajustes", command=configure_email_settings)
config_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Crear botón "Comenzar/Parar"
start_stop_button = tk.Button(frame, text="Iniciar", command=start_monitoring)
start_stop_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")

# Configuración de la ventana
window.geometry("490x528")
window.protocol("WM_DELETE_WINDOW", lambda: (save_hosts_seen(), save_last_alert_time(), window.quit()))

# Crear la ventana de status
status_window = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=10)
status_window.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Cargar la última alerta al inicio de la aplicación
last_alert_time = load_last_alert_time()

# Cargar la última subnet ingresada por el usuario
last_subnet = load_last_subnet()
subnet_entry.insert(0, last_subnet)

# Iniciar el monitoreo automáticamente al abrir la aplicación
start_monitoring()

# Loop principal de la aplicación
window.mainloop()