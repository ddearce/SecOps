<h1 align="center">Event Extractor</h1>

<p align="center">
  <img src="extractor.png" alt="Extractor Logo" width="200">
</p>

<p align="center">
  <em>Keeping things organized and in order.</em>
</p>

---

## Descripción

SECOPS - Event Extractor es una herramienta de línea de comandos diseñada por Damian de Arce para extraer eventos del Visor de Eventos de Windows en la categoría de seguridad y exportarlos a un archivo Excel. Esta herramienta facilita el análisis de eventos de seguridad críticos en un sistema Windows.

---

## Descargo de Responsabilidad

**IMPORTANTE**: Damian de Arce no se hace responsable por el mal uso de esta herramienta ni por cualquier problema que pueda surgir como resultado de su uso. El usuario asume toda la responsabilidad y riesgo al utilizar esta herramienta. Antes de usarla, asegúrate de tener permisos adecuados y comprende los posibles impactos de su uso en tu sistema.

---

## Requisitos

- Python 3.x
- Biblioteca `pandas`
- Permisos de administrador para acceder a los registros de eventos de Windows

---

## Instalación

1. Clona o descarga este repositorio en tu sistema.

2. Asegúrate de tener Python 3.x instalado.

3. Instala la biblioteca `pandas` ejecutando el siguiente comando:
   
pip install pandas


---

## Uso

1. Abre una terminal con permisos de administrador.

2. Navega al directorio donde se encuentra la herramienta.

3. Ejecuta el script `event.py` usando Python:

python event.py


4. Aparecerá el título y el descargo de responsabilidad. Debes aceptar el descargo de responsabilidad para continuar.

5. La herramienta extraerá los eventos de seguridad del Visor de Eventos de Windows y los exportará a un archivo Excel llamado "SecurityEvents.xlsx" en el mismo directorio.

6. Los eventos exportados se presentarán en columnas que incluyen palabras clave, fecha y hora, origen, ID del evento, categoría de la tarea y detalles.

---

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar esta herramienta, no dudes en crear un pull request o reportar problemas.

---

## Licencia

Este proyecto está bajo la Licencia MIT.

---

¡Esperamos que SECOPS - Event Extractor te sea útil en tu trabajo de seguridad y análisis de eventos de Windows!

