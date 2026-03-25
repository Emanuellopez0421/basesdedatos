from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Conexión MongoDB Atlas
MONGO_URI = "mongodb+srv://esp32:esp32pass@tecemmanuel.fbacjvy.mongodb.net/iot"

client = MongoClient(MONGO_URI)
db = client.iot
collection = db.sensores

@app.get("/")
def root():
    return {"mensaje": "API funcionando. Usa POST en /sensor para enviar datos."}

@app.post("/sensor")
def guardar_sensor(data: dict):
    # Creamos una copia para añadir la fecha sin ensuciar el objeto original
    nuevo_registro = {
        "temperatura": data.get("temperatura"),
        "humedad": data.get("humedad"),
        "fecha": datetime.now()
    }

    # Insertar en MongoDB
    resultado = collection.insert_one(nuevo_registro)

    # Devolvemos una respuesta limpia
    return {
        "status": "dato guardado",
        "id_insertado": str(resultado.inserted_id),
        "valor_temp": data.get("temperatura")
    }
