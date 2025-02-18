import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration de la connexion InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "my-secret-token"
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "my-bucket"

# Connexion à InfluxDB
client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Chemin du fichier contenant les données
FILENAME = "data/air-sensor-data.txt"

def parse_line_protocol(line):
    """Parse une ligne du fichier InfluxDB et retourne un objet Point."""
    try:
        parts = line.strip().split(" ")
        measurement, tags_fields = parts[0], parts[1:]
        
        # Extraire les tags
        tags = {}
        tag_parts = measurement.split(",")
        measurement_name = tag_parts[0]  # Ex: "airSensors"
        for tag in tag_parts[1:]:
            key, value = tag.split("=")
            tags[key] = value
        
        # Extraire les champs
        fields = {}
        timestamp = None
        for part in tags_fields:
            if "=" in part:
                key, value = part.split("=")
                fields[key] = float(value)  # Convertir les valeurs en float
            else:
                timestamp = int(part)  # Dernière partie = timestamp
        
        # Créer un point InfluxDB
        point = influxdb_client.Point(measurement_name).time(timestamp)
        for key, value in tags.items():
            point = point.tag(key, value)
        for key, value in fields.items():
            point = point.field(key, value)
        
        return point
    except Exception as e:
        print(f"⚠️ Erreur de parsing : {e} (ligne ignorée)")
        return None

def import_data():
    """Lit le fichier et insère les données dans InfluxDB."""
    print("📡 Début de l'importation des données...")

    with open(FILENAME, "r") as file:
        for line in file:
            point = parse_line_protocol(line)
            if point:
                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
                print(f"✅ Donnée insérée : {point.to_line_protocol()}")

    print("✅ Importation terminée.")

if __name__ == "__main__":
    import_data()
    client.close()