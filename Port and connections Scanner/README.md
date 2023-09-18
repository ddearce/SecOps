# Port Scanner by Damian de Arce

---

## Descripción

Port Scanner es una herramienta de escaneo de puertos desarrollada por Damian de Arce. 
Esta herramienta permite a los usuarios escanear puertos en un host especificado y mostrar el estado de los puertos (abiertos o cerrados). 
Además, muestra conexiones activas y las IP a las que están conectadas.

---

## Descargo de Responsabilidad

**IMPORTANTE**: Esta herramienta de escaneo de puertos se proporciona "tal cual" y está basada en el mejor esfuerzo. 
Damian de Arce no se hace responsable por los resultados ni los daños que esta herramienta pudiera ocasionar. 
El usuario asume toda la responsabilidad y riesgo al utilizar esta herramienta. 
Antes de utilizarla, asegúrese de comprender los posibles impactos y aceptar el riesgo.

---

## Requisitos

- Python 3.x
- Bibliotecas `pygame`, `socket`, `tqdm`, y `psutil`

---

## Instalación

1. Clona o descarga este repositorio en tu sistema.

2. Asegúrate de tener Python 3.x instalado.

3. Instala las bibliotecas requeridas utilizando `pip`:

pip install pygame tqdm psutil


---

## Uso

1. Ejecuta el script `port_scanner.py` utilizando Python:

python port_scanner.py

2. Se mostrará una presentación animada.

3. Ingresa el host que deseas escanear y presiona "Enter" para iniciar el escaneo de puertos.

4. La herramienta escaneará puertos desde el puerto 1 hasta el 65535 y mostrará el estado de cada puerto (abierto o cerrado).

5. Además, mostrará conexiones activas y las IP a las que están conectadas.

6. Los resultados del escaneo se guardarán en un archivo de texto llamado "resultados.txt" en la raíz del directorio.

7. La música de fondo se detendrá al finalizar el escaneo.

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta herramienta, no dudes en crear un pull request o reportar problemas.

---

## Licencia

Este proyecto está bajo la Licencia MIT.

---

¡Gracias por utilizar Port Scanner by Damian de Arce!

