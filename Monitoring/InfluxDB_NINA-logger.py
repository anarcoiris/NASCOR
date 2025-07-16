import os
import re
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision

# ⚙️ CONFIGURA ESTOS PARÁMETROS
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "tu_token"
INFLUX_ORG = "tu_org"
INFLUX_BUCKET = "nina_logs"

# Ruta a los logs de NINA
LOG_FOLDER = os.path.expandvars(r"C:\Users\soyko\AppData\Local\NINA\Logs")

def get_latest_log_file(folder):
    files = [f for f in os.listdir(folder) if f.endswith(".log")]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return os.path.join(folder, files[0]) if files else None

def parse_log_line(line):
    # Ejemplo de línea: [2024-07-10T23:41:52.839] [INFO] Exposure 120s started...
    match = re.match(r"\[(.*?)\].*Exposure (\d+)[sS].*", line)
    if match:
        timestamp_str, exposure_sec = match.groups()
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", ""))
        return timestamp, int(exposure_sec)
    return None, None

def send_to_influx(timestamp, duration):
    with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
        write_api = client.write_api()
        point = Point("exposure")\
            .field("duration_sec", duration)\
            .time(timestamp, WritePrecision.NS)
        write_api.write(bucket=INFLUX_BUCKET, record=point)

def main():
    log_file = get_latest_log_file(LOG_FOLDER)
    if not log_file:
        print("No se encontró ningún log.")
        return

    print(f"Leyendo: {log_file}")
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            timestamp, duration = parse_log_line(line)
            if timestamp:
                print(f"Exposure {duration}s at {timestamp}")
                send_to_influx(timestamp, duration)

if __name__ == "__main__":
    main()
