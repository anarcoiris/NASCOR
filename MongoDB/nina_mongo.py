import requests
import time
from prometheus_client import start_http_server, Gauge
from pymongo import MongoClient
from datetime import datetime
from datetime import timezone

# Configura MongoDB
mongo_client = MongoClient("mongodb://root:root@localhost:27017/?authSource=admin")
db = mongo_client["nina_monitor"]
collection = db["nina_metrics"]
guider_collection = db["guider_metrics"]

# Gauges Prometheus
altitude_gauge = Gauge("nina_mount_altitude_degrees", "Altitud del telescopio (en grados)")
azimuth_gauge = Gauge("nina_mount_azimuth_degrees", "Acimut del telescopio (en grados)")
ra_gauge = Gauge("nina_mount_right_ascension_hours", "Ascensión recta del telescopio (en horas)")
dec_gauge = Gauge("nina_mount_declination_degrees", "Declinación del telescopio (en grados)")
target_name_gauge = Gauge("nina_mount_target_name_length", "Longitud del nombre del target")  # como workaround
connected_gauge = Gauge("nina_mount_connected", "¿Está conectada la montura? (1 = sí, 0 = no)")
sidereal_time_gauge = Gauge("nina_mount_sidereal_time", "Tiempo sideral actual")

# (Opcional) Gauges para guía
rms_total_gauge = Gauge("nina_guider_rms_total", "RMS total del guiado")
rms_ra_gauge = Gauge("nina_guider_rms_ra", "RMS en RA")
rms_dec_gauge = Gauge("nina_guider_rms_dec", "RMS en DEC")

# Inicia servidor Prometheus local en puerto 9101
start_http_server(9101)

def fetch_nina_data():
    try:
        r = requests.get("http://192.168.1.138:1888/v2/api/equipment/mount/info")  # cambia a tu puerto real
        data = r.json()

        mount = data.get("Response", {})
        telescope = {
            "altitude": data.get("Altitude", 0.0),
            "azimuth": data.get("Azimuth", 0.0),
            "ra": data.get("RightAscension", 0.0),
            "dec": data.get("Declination", 0.0),
            "sidereal_time": data.get("SiderealTime", 0.0),
            "connected": int(data.get("Connected", False)),
            "timestamp": datetime.now(timezone.utc)
        }

        # Actualiza métricas Prometheus
        altitude_gauge.set(telescope["altitude"])
        azimuth_gauge.set(telescope["azimuth"])
        ra_gauge.set(telescope["ra"])
        dec_gauge.set(telescope["dec"])
        target_name_gauge.set(len(telescope["target_name"]))  # workaround: Prometheus no permite strings
        connected_gauge.set(telescope["connected"])

        # Inserta en MongoDB
        telescope["timestamp"] = datetime.utcnow()
        collection.insert_one(telescope)

    except Exception as e:
        print(f"[!] Error al obtener datos de NINA o insertar en MongoDB: {e}")

def fetch_guider_data():
    try:
        r = requests.get("http://192.168.1.138:1888/v2/api/equipment/guider/graph", timeout=5)
        data = r.json().get("Response", {})

        rms = data.get("RMS", {})

        guider = {
            "rms_total": rms.get("Total", 0.0),
            "rms_ra": rms.get("RA", 0.0),
            "rms_dec": rms.get("Dec", 0.0),
            "peak_ra": rms.get("PeakRA", 0.0),
            "peak_dec": rms.get("PeakDec", 0.0),
            "scale": rms.get("Scale", 0.0),
            "data_points": rms.get("DataPoints", 0),
            "interval": data.get("Interval", 0),
            "timestamp": datetime.now(timezone.utc)
        }

        # Actualiza métricas Prometheus
        rms_total_gauge.set(guider["rms_total"])
        rms_ra_gauge.set(guider["rms_ra"])
        rms_dec_gauge.set(guider["rms_dec"])

        # Inserta en MongoDB
        guider_collection.insert_one(guider)

    except Exception as e:
        print(f"[!] Error al obtener datos del guiado: {e}")

if __name__ == "__main__":
    print("[+] Iniciando exporter NINA (montura + guía) con MongoDB...")
    while True:
        fetch_nina_data()
        fetch_guider_data()
        time.sleep(5)