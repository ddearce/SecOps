<h1 align="center">FileSentry: Your File Guardian</h1>

<p align="center">
  <img src="filesentry.png" alt="FileSentry Logo" width="200">
</p>

<p align="center">
  <em>Keep a watchful eye on your critical files and get notified of unexpected changes.</em>
</p>

---

FileSentry is a Python tool that allows you to maintain constant vigilance over your critical files and notifies you via email when unexpected changes are detected. This tool is essential for cybersecurity professionals and system administrators who want to maintain control over the integrity of their important files.

**FileSentry es una herramienta de Python que te permite mantener un ojo vigilante sobre tus archivos críticos y te notifica por correo electrónico cuando se detectan cambios inesperados. Esta herramienta es esencial para profesionales de la ciberseguridad y administradores de sistemas que desean mantener un control constante sobre la integridad de sus archivos importantes.**

---

## Features / Características

- Real-time monitoring of critical files / Monitoreo en tiempo real de archivos críticos.
- Detects changes in file content or metadata / Detecta cambios en el contenido o metadatos del archivo.
- Sends email notifications when a change is detected / Envía notificaciones por correo electrónico cuando se detecta un cambio.
- Customizable to suit your security needs / Personalizable para adaptarse a tus necesidades de seguridad.

## Configuration / Configuración

Before using FileSentry, make sure to configure your email credentials in the script. This will allow you to receive email notifications when changes in files are detected. Additionally, provide the paths of the directories you wish to monitor in the `directorios_a_monitorear` variable.

**Antes de usar FileSentry, asegúrate de configurar tus credenciales de correo electrónico en el script. Esto te permitirá recibir notificaciones por correo electrónico cuando se detecten cambios en los archivos. Además, debes proporcionar la ruta de los directorios que deseas monitorear en la variable `directorios_a_monitorear`.**

## Usage / Uso

1. Clone this repository to your local system / Clona este repositorio en tu sistema local.
2. Configure your email credentials in the script / Configura tus credenciales de correo electrónico en el script.
3. Add the paths of the directories you wish to monitor to the `directorios_a_monitorear` variable / Agrega las rutas de los directorios que deseas monitorear en la variable `directorios_a_monitorear`.
4. Run the `filesentry.py` script using Python / Ejecuta el script `filesentry.py` utilizando Python.

\```
python filesentry.py
\```

FileSentry will start monitoring the specified directories and will notify you via email when unexpected changes in the files are detected.

FileSentry comenzará a monitorear los directorios especificados y te notificará por correo electrónico cuando detecte cambios inesperados en los archivos.

## Contributions / Contribuciones
If you have ideas to enhance FileSentry or encounter issues, we invite you to contribute! Feel free to open issues or send pull requests to make this tool even better.

Si tienes ideas para mejorar FileSentry o encuentras problemas, ¡te invitamos a contribuir! Siéntete libre de abrir problemas (issues) o enviar solicitudes de extracción (pull requests) para hacer que esta herramienta sea aún mejor.

## Notes / Notas
Use this tool ethically and legally, and respect all applicable laws and regulations / Utiliza esta herramienta de manera ética y legal y respeta todas las leyes y regulaciones aplicables.
Exercise caution when storing passwords in code. It is recommended to use secure methods for managing credentials in production environments / Ten precaución al almacenar contraseñas en el código. Se recomienda utilizar métodos seguros para gestionar las credenciales en entornos de producción.

## License / Licencia
This project is licensed under the MIT License. See the LICENSE file for more details.

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para obtener más detalles.
