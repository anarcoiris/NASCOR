#!/usr/bin/env python3
import sys

# recibiremos el texto por consola
for line in sys.stdin:
    # eliminamos espacios sobrantes
    line = line.strip()
    # dividimos la linea en palabras
    words = line.split()
    # para cada palabra
    for word in words:
        # escribiremos por consola, la pareja clave-valor 
        # que entrará al reducer: <word, 1>
        print ('%s\t%s' % (word, 1))
