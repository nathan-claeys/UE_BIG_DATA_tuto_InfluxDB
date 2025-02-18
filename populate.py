import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration de la connexion InfluxDB
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "my-secret-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "my-bucket"

# Connexion à InfluxDB
client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Chemin du fichier contenant les données
FILENAME = "data/air-sensor-data.txt"

def import_data():
    print("📡 Début de l'importation des données...")

    with open(FILENAME, "r") as file:
        for line in file:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=line)

    print("✅ Importation terminée.")

if __name__ == "__main__":
    import_data()
    client.close()