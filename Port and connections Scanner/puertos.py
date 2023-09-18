import pygame
import socket
from tqdm import tqdm
import psutil
import threading

# Initialize pygame
pygame.init()

open_ports = []

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    result = sock.connect_ex((host, port))
    if result == 0:
        open_ports.append(port)
        print("Port {}:  Open".format(port))
    else:
        print("Port {}:  Closed".format(port))
    sock.close()

def check_ports(host, start_port, end_port):
    threads = []
    for port in range(start_port, end_port):
        t = threading.Thread(target=scan_port, args=(host, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    connections = psutil.net_connections()
    # Iterar sobre las conexiones y mostrar las conexiones activas y las IPs a las que están conectadas
    for conn in connections:
        if conn.status == "ESTABLISHED":
            print("Conexión activa: ", conn.laddr, "->", conn.raddr)
    
    # Guardar en un archivo
    with open("resultados.txt", "w") as f:
        f.write("Puerto\t Estado\t Conexión\n")
        for p in open_ports:
            f.write("{}\t Open\n".format(p))
        for p in range(start_port, end_port):
            if p not in open_ports:
                f.write("{}\t Closed\n".format(p))
        for conn in connections:
            if conn.status == "ESTABLISHED":
                f.write("\t\t {} -> {} \n".format(conn.laddr,conn.raddr))
    return open_ports

# Cargar y reproducir música
pygame.mixer.music.load("music.ogg")
pygame.mixer.music.play()


# Mostrar presentación animada
print("Escaneador de puertos by Damian de Arce - Cybersecurity Specialist")
print("Escribe el host y presiona enter para iniciar: ")
host = input()

# Escanear puertos
start_port = 1
end_port = 65535
check_ports(host, start_port, end_port)

# Detener la música
pygame.mixer.music.stop()
