import hashlib
import itertools
import multiprocessing

# Constantes
target_hash = "925ab3ca8e94506ea0f2a14ede580194"
salt = "salt1"
NUM_PROCESOS = 12

def check_hashes(prefixes_chunk):
    for prefix in prefixes_chunk:
        for num in range(10000):
            intento = f"{prefix}{num:04d}"
            hashed = hashlib.md5((intento + salt).encode()).hexdigest()

            if hashed == target_hash:
                print(f"¡Ripped!: {intento}")
                return intento  # Devuelve en cuanto lo encuentra
    return None


def chunkify(iterable, n):
    """Divide una lista en n partes aproximadamente iguales"""
    k, m = divmod(len(iterable), n)
    return [iterable[i*k + min(i, m):(i+1)*k + min(i+1, m)] for i in range(n)]


def main():
    letras = 'abcdefghijklmnopqrstuvwxyz'
    all_prefixes = [''.join(p) for p in itertools.product(letras, repeat=3)]  # aaa - zzz

    # Divide el trabajo en chunks para cada proceso
    chunks = chunkify(all_prefixes, NUM_PROCESOS)

    with multiprocessing.Pool(NUM_PROCESOS) as pool:
        results = pool.map(check_hashes, chunks)

    # Buscar cuál resultó en éxito
    for result in results:
        if result:
            print(f"Contraseña encontrada: {result}")
            break
    else:
        print("Solo es una batalla, no la guerra.")


if __name__ == "__main__":
    main()
