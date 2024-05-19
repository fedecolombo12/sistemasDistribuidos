import random
from datetime import datetime, timedelta
import time
from prometheus_client import start_http_server, Gauge

# Definir los rangos para cada atributo
date_range_start = datetime(2024, 1, 1)
date_range_end = datetime(2024, 1, 2)  # Ajustado a un solo día para este ejemplo
site_names = ['Site1', 'Site2', 'Site3']
max_sensor_id_per_site = 3  # Ajustar este valor según la cantidad máxima de sensores por sitio
sensor_types = ['Tipo1', 'Tipo2', 'Tipo3']
soil_moisture_range = (5, 70)
temperature_range_summer = (10, 40)  # Verano en Uruguay
temperature_range_winter = (-5, 25)   # Invierno en Uruguay

# Inicializar métricas
soil_moisture_metric = Gauge('soil_moisture', 'Soil Moisture', ['site_name', 'sensor_id', 'sensor_type'])
air_temperature_metric = Gauge('air_temperature', 'Air Temperature', ['site_name', 'sensor_id', 'sensor_type'])

# Función para generar un registro de datos aleatorios para un sensor específico
def generate_sensor_data(site_id, sensor_id, sensor_type, date):
    site_name = site_names[site_id]
    soil_moisture = round(random.uniform(soil_moisture_range[0], soil_moisture_range[1]), 1)
    if date.month in [12, 1, 2]:  # Si es verano
        air_temperature = round(random.uniform(temperature_range_summer[0], temperature_range_summer[1]), 1)
    else:  # Si es invierno
        air_temperature = round(random.uniform(temperature_range_winter[0], temperature_range_winter[1]), 1)
    
    # Actualizar métricas
    soil_moisture_metric.labels(site_name=site_name, sensor_id=sensor_id, sensor_type=sensor_type).set(soil_moisture)
    air_temperature_metric.labels(site_name=site_name, sensor_id=sensor_id, sensor_type=sensor_type).set(air_temperature)

# Generar los IDs únicos para cada sitio y asignar tipos de sensor
sensor_ids_by_site = {}
sensor_type_by_id = {}
current_sensor_id = 1
for site_id in range(len(site_names)):
    sensor_ids_by_site[site_id] = list(range(current_sensor_id, current_sensor_id + max_sensor_id_per_site))
    for sensor_id in sensor_ids_by_site[site_id]:
        sensor_type_by_id[sensor_id] = random.choice(sensor_types)
    current_sensor_id += max_sensor_id_per_site

# Iniciar el servidor HTTP para exponer métricas
start_http_server(8000)

# Generar datos para múltiples sensores y actualizar las métricas cada 10 segundos
current_date = date_range_start
while current_date <= date_range_end:
    iteration_start_time = time.time()
    for site_id in range(len(site_names)):
        for sensor_id in sensor_ids_by_site[site_id]:
            sensor_type = sensor_type_by_id[sensor_id]
            generate_sensor_data(site_id, sensor_id, sensor_type, current_date)
    current_date += timedelta(seconds=10)  # Avanzar 10 segundos antes de generar el siguiente dato
    time_to_next_iteration = 10 - (time.time() - iteration_start_time)
    if time_to_next_iteration > 0:
        time.sleep(time_to_next_iteration)  # Esperar hasta que se cumplan los 10 segundos de la iteración actual
