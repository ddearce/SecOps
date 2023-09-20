import random
import string
import tkinter as tk
from tkinter import ttk
import pyperclip

def generate_password(length, include_special_chars=True):
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_button_clicked():
    length = int(length_entry.get())
    include_special_chars = special_chars_var.get()

    password = generate_password(length, include_special_chars)
    password_entry.delete(0, tk.END)  # Borrar el contenido anterior
    password_entry.insert(0, password)

def copy_button_clicked():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        result_label.config(text="Password copied to clipboard!")
    else:
        result_label.config(text="Generate a password first!")

# Crear la ventana principal
root = tk.Tk()
root.title("SecurePassGen - Developed by Damian de Arce")
root.geometry("430x200")  # Ajustar el tamaño de la ventana

# Crear y configurar etiquetas y entradas
length_label = ttk.Label(root, text="Enter the desired password length:")
length_entry = ttk.Entry(root)
length_entry.insert(0, "12")

special_chars_var = tk.BooleanVar()
special_chars_checkbutton = ttk.Checkbutton(root, text="Include special characters", variable=special_chars_var, onvalue=True, offvalue=False)

generate_button = ttk.Button(root, text="Generate Password", command=generate_button_clicked)
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_button_clicked)
password_entry = ttk.Entry(root)
result_label = ttk.Label(root, text="")

# Colocar widgets en la ventana
length_label.pack()
length_entry.pack()
special_chars_checkbutton.pack()
generate_button.pack()
password_entry.pack()
copy_button.pack()
result_label.pack()

root.mainloop()

