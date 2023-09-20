from cryptography.fernet import Fernet
import sys
import os

# Genera una clave de cifrado única
def generar_clave():
    return Fernet.generate_key()

# Cifra un archivo
def cifrar_archivo(clave, nombre_archivo):
    fernet = Fernet(clave)
    with open(nombre_archivo, 'rb') as archivo:
        datos = archivo.read()
    datos_cifrados = fernet.encrypt(datos)
    with open(nombre_archivo + '.cifrado', 'wb') as archivo_cifrado:
        archivo_cifrado.write(datos_cifrados)
    os.remove(nombre_archivo)

# Descifra un archivo cifrado
def descifrar_archivo(clave, nombre_archivo_cifrado):
    fernet = Fernet(clave)
    with open(nombre_archivo_cifrado, 'rb') as archivo_cifrado:
        datos_cifrados = archivo_cifrado.read()
    datos_descifrados = fernet.decrypt(datos_cifrados)
    with open(nombre_archivo_cifrado[:-8], 'wb') as archivo_descifrado:
        archivo_descifrado.write(datos_descifrados)
    os.remove(nombre_archivo_cifrado)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python cipherfileguard.py [encrypt/decrypt] [nombre_archivo]")
        sys.exit(1)

    operacion = sys.argv[1]
    nombre_archivo = sys.argv[2]

    if operacion == 'encrypt':
        clave = generar_clave()
        with open('clave.key', 'wb') as clave_file:
            clave_file.write(clave)
        cifrar_archivo(clave, nombre_archivo)
        print(f"El archivo '{nombre_archivo}' ha sido cifrado correctamente.")
    elif operacion == 'decrypt':
        try:
            with open('clave.key', 'rb') as clave_file:
                clave = clave_file.read()
            descifrar_archivo(clave, nombre_archivo)
            print(f"El archivo '{nombre_archivo}' ha sido descifrado correctamente.")
        except FileNotFoundError:
            print("No se encontró la clave de cifrado. Debes cifrar el archivo antes de descifrarlo.")
    else:
        print("Operación no válida. Use 'encrypt' o 'decrypt'.")
