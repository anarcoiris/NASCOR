#!/usr/bin/env python3
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None

# recibiremos la entrada por consola
for line in sys.stdin:
    # eliminamos espacios sobrantes
    line = line.strip()
    # separamos la palabra y el número que nos llega
    word, count = line.split('\t', 1)

    # convertimos el número a integer
    try:
        count = int(count)
    except ValueError:
        # descartamos si falla
        continue

    # las palabras llegan ordenadas alfabéticamente por hadoop
    # sumamos el valor si la palabra es la misma que la anterior
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # y si no, escribimos por consola el resultado
            print ('%s\t%s' % (current_word, current_count))

		  # y pasamos a la siguiente palabra
        current_count = count
        current_word = word

# imprimimos la ultima palabra!
if current_word == word:
    print ('%s\t%s' % (current_word, current_count))
