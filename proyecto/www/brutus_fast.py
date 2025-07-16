import hashlib
import itertools
import string
import multiprocessing
import argparse

# --- Argumentos CLI ---
parser = argparse.ArgumentParser(description="Cracker optimizado alfanumérico con hash + salt")
parser.add_argument("--hash", required=True, help="Hash objetivo (MD5)")
parser.add_argument("--salt", required=True, help="Salt objetivo")
parser.add_argument("--min-len", type=int, default=6, help="Longitud mínima")
parser.add_argument("--max-len", type=int, default=7, help="Longitud máxima")
parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count()-8, help="Número de procesos")
args = parser.parse_args()

# --- Caracteres permitidos ---
CHARS = string.ascii_lowercase + string.digits  # 36 caracteres

# --- Generador de contraseñas al vuelo (no carga en RAM) ---
def password_generator(min_len, max_len):
    for length in range(min_len, max_len + 1):
        for pwd_tuple in itertools.product(CHARS, repeat=length):
            yield ''.join(pwd_tuple)

# --- Función que evalúa 1 contraseña ---
def try_password(password):
    h = hashlib.md5((password + args.salt).encode()).hexdigest()
    if h == args.hash:
        print(f"\n🎯 Contraseña encontrada: {password}")
        return password
    return None

# --- Main cracking ---
def main():
    print(f"🔍 Iniciando búsqueda con longitud {args.min_len} a {args.max_len}...")
    print(f"🧠 Usando {args.workers} procesos con generador por streaming")

    with multiprocessing.Pool(args.workers) as pool:
        for result in pool.imap_unordered(try_password, password_generator(args.min_len, args.max_len), chunksize=1000):
            if result:
                print(f"✅ ¡Éxito!: {result}")
                pool.terminate()
                return

    print("❌ Contraseña no encontrada.")

if __name__ == "__main__":
    main()
