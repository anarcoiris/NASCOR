import pymongo
import json

cliente = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
db = cliente["catalogo"]
coleccion_productos = db["productos"]

# Abrir y leer el archivo JSON
'''
with open('productos.json', 'r', encoding='utf-8') as archivo: 
    datos = json.load(archivo)
    coleccion_productos.insert_many(datos)
    print("Productor insertados")
'''

#Consulta para productos con stock menor a 10
filter={
    'stock': {
        '$lt': 10
    }
}
result = coleccion_productos.find(
  filter=filter
)

print(list(result))


#Suma stock

result = coleccion_productos.aggregate([
    {
        '$group': {
            '_id': None, 
            'sumaStock': {
                '$sum': '$stock'
            }
        }
    }
])

for doc in result:
    print("Suma total de stock:", doc['sumaStock'])