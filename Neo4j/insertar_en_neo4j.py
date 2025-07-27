from neo4j import GraphDatabase
import json
import random
from datetime import datetime

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(user, password))

with open("clientes.json", "r", encoding="utf-8") as f:
    clientes = json.load(f)

with open("productos.json", "r", encoding="utf-8") as f:
    productos = json.load(f)

def insertar_datos(tx):
    for cliente in clientes:
        tx.run("MERGE (c:Cliente {email: $email}) "
               "SET c.nombre = $nombre, c.edad = $edad",
               nombre=cliente["nombre"], email=cliente["email"], edad=cliente["edad"])

    for producto in productos:
        tx.run("MERGE (p:Producto {nombre: $nombre}) "
               "SET p.categoria = $categoria",
               nombre=producto["nombre"], categoria=producto["categoria"])

    for cliente in clientes:
        comprados = random.sample(productos, random.randint(1, 3))
        for prod in comprados:
            tx.run(
                "MATCH (c:Cliente {email: $email}), (p:Producto {nombre: $producto}) "
                "MERGE (c)-[:COMPRA {fecha: date($fecha)}]->(p)",
                email=cliente["email"], producto=prod["nombre"],
                fecha=datetime.now().strftime("%Y-%m-%d")
            )

with driver.session() as session:
    session.execute_write(insertar_datos)

print("Datos insertados en Neo4j correctamente.")