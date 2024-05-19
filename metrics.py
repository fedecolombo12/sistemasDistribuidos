from prometheus_client import start_http_server, Gauge
import random
import time

# Definir las métricas
soil_moisture_metric = Gauge('soil_moisture', 'Soil Moisture', ['sensor_id'])
air_temperature_metric = Gauge('air_temperature', 'Air Temperature', ['sensor_id'])

# Iniciar el servidor de métricas en el puerto 8000
start_http_server(8000)

# Generar datos aleatorios y actualizar las métricas
sensor_ids = range(1, 4)
while True:
    for sensor_id in sensor_ids:
        soil_moisture_metric.labels(sensor_id=sensor_id).set(random.uniform(5, 70))
        air_temperature_metric.labels(sensor_id=sensor_id).set(random.uniform(10, 40))
    time.sleep(10)  # Actualizar cada 10 segundos
