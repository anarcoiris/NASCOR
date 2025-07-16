import hashlib
import itertools

target_hash = "925ab3ca8e94506ea0f2a14ede580194"
salt = "salt1"

# Genera todos los prefijos de tres letras (aaa...zzz)
letters = 'abcdefghijklmnopqrstuvwxyz'
for prefix_tuple in itertools.product(letters, repeat=3):
    prefix = ''.join(prefix_tuple)

    for num in range(10000):  # desde 0000 hasta 9999
        intento = f"{prefix}{num:04d}"
        hashed = hashlib.md5((intento + salt).encode()).hexdigest()

        if hashed == target_hash:
            print(f"¡Ripped!: {intento}")
            exit()

print("Solo es una batalla, no la guerra.")
