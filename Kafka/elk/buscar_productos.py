from elasticsearch import Elasticsearch
import json

# Conexión
es = Elasticsearch("http://localhost:9200")

# Crear índice si no existe
if not es.indices.exists(index="productos"):
    es.indices.create(index="productos")

# Cargar productos
with open("productos.json", "r", encoding="utf-8") as f:
    productos = json.load(f)

# Indexar productos
for i, prod in enumerate(productos):
    es.index(index="productos", id=i+1, document=prod)

print("Productos indexados correctamente.")

# Búsqueda por texto
query = {
    "query": {
        "match": {
            "descripcion": "retroiluminación"
        }
    }
}
result = es.search(index="productos", body=query)
print("Resultados de búsqueda:")
for hit in result["hits"]["hits"]:
    print(hit["_source"])