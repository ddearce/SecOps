import os
import pandas as pd
import ctypes
from datetime import datetime

# Función para obtener los detalles del evento
def get_event_details(handle, event):
    data = ""
    buffer_size = 2048
    buffer = ctypes.create_string_buffer(buffer_size)
    
    try:
        # Leer los datos del evento
        bytes_read = ctypes.c_ulong(0)
        ctypes.windll.advapi32.EvtRender(
            None, handle, 2, buffer_size, buffer, ctypes.byref(bytes_read), None
        )
        
        # Convertir los datos en una cadena
        data = buffer.value.decode("utf-8", errors="ignore")
    except Exception as e:
        data = f"Error al obtener detalles del evento: {str(e)}"
    return data

# Función principal para extraer eventos de seguridad
def extract_security_events_to_excel():
    # Crear un DataFrame para almacenar los eventos
    events_df = pd.DataFrame(columns=["Palabras Clave", "Fecha y Hora", "Origen", "Id del Evento", "Categoría de la Tarea", "Detalles"])
    
    # Abrir el registro de eventos de seguridad
    handle = ctypes.windll.advapi32.EvtOpenLog(None, "Security", 0x1)
    
    # Recorrer los eventos
    while True:
        events = ctypes.windll.advapi32.EvtNext(handle, 1, None, 0, 0, None)
        if not events:
            break
        
        for event in events:
            event_id = ctypes.windll.advapi32.EvtGetEventId(event)
            event_time = ctypes.windll.advapi32.EvtGetLogInfo(event, 4).decode("utf-8", errors="ignore")
            event_source = ctypes.windll.advapi32.EvtGetPublisherId(event).decode("utf-8", errors="ignore")
            event_task_category = ctypes.windll.advapi32.EvtGetPublisherProperty(event, 4).decode("utf-8", errors="ignore")
            event_keywords = ctypes.windll.advapi32.EvtGetPublisherProperty(event, 5).decode("utf-8", errors="ignore")
            event_details = get_event_details(handle, event)
            
            events_df = events_df.append({
                "Palabras Clave": event_keywords,
                "Fecha y Hora": event_time,
                "Origen": event_source,
                "Id del Evento": event_id,
                "Categoría de la Tarea": event_task_category,
                "Detalles": event_details
            }, ignore_index=True)
    
    # Cerrar el registro de eventos
    ctypes.windll.advapi32.EvtClose(handle)
    
    # Exportar los eventos a un archivo Excel
    output_file = "SecurityEvents.xlsx"
    events_df.to_excel(output_file, index=False)
    
    return output_file

if __name__ == "__main__":
    # Mostrar el título vistoso
    print("SECOPS - Event Extractor by Damian de Arce")
    
    # Mostrar el descargo de responsabilidad
    disclaimer = """
    Descargo de Responsabilidad:
    Damian de Arce no se hace responsable por el mal uso de esta herramienta ni por cualquier problema que pueda surgir como resultado de su uso. El usuario asume toda la responsabilidad y riesgo al utilizar esta herramienta.
    """
    print(disclaimer)
    
    # Solicitar aceptación del descargo de responsabilidad
    aceptar_descargo = input("¿Aceptas el descargo de responsabilidad? (Sí/No): ")
    
    if aceptar_descargo.lower() == "si":
        # Extraer eventos y exportar a Excel
        output_file = extract_security_events_to_excel()
        print(f"Los eventos de seguridad se han exportado correctamente en '{output_file}' en el mismo directorio que el script.")
    else:
        print("No puedes continuar sin aceptar el descargo de responsabilidad.")
