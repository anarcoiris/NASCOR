import json

# Leer el archivo JSON original
with open('productos.json', 'r', encoding='utf-8') as f:
    productos = json.load(f)

# Crear el archivo NDJSON para _bulk
with open('productos_bulk.ndjson', 'w', encoding='utf-8') as f_bulk:
    for producto in productos:
        # Línea de acción (indexación)
        accion = { "index": { "_index": "productos" } }
        f_bulk.write(json.dumps(accion) + '\n')
        
        # Línea de documento
        f_bulk.write(json.dumps(producto) + '\n')

print("Archivo productos_bulk.ndjson generado correctamente.")
