from flask import Flask
from flask_graphql import GraphQLView
import graphene
import requests
import flask
app = Flask(__name__)

# Definir el tipo SensorData
class SensorData(graphene.ObjectType):
    sensor_id = graphene.Int()
    soil_moisture = graphene.Float()
    air_temperature = graphene.Float()

# Función para consultar Prometheus
def query_prometheus(sensor_id):
    prometheus_url = 'http://localhost:9090/api/v1/query'
    
    # Consulta para la humedad del suelo
    soil_moisture_query = f'soil_moisture{{sensor_id="{sensor_id}"}}'
    soil_moisture_response = requests.get(prometheus_url, params={'query': soil_moisture_query})
    soil_moisture_result = soil_moisture_response.json()['data']['result'][0]
    soil_moisture = float(soil_moisture_result['value'][1])
    
    # Consulta para la temperatura del aire
    air_temperature_query = f'air_temperature{{sensor_id="{sensor_id}"}}'
    air_temperature_response = requests.get(prometheus_url, params={'query': air_temperature_query})
    air_temperature_result = air_temperature_response.json()['data']['result'][0]
    air_temperature = float(air_temperature_result['value'][1])
    
    return soil_moisture, air_temperature

# Definir la consulta GraphQL
class Query(graphene.ObjectType):
    get_sensor_data = graphene.Field(SensorData, sensor_id=graphene.Int(required=True))

    def resolve_get_sensor_data(self, info, sensor_id):
        # Obtener los datos de Prometheus
        soil_moisture, air_temperature = query_prometheus(sensor_id)

        return SensorData(
            sensor_id=sensor_id,
            soil_moisture=soil_moisture,
            air_temperature=air_temperature
        )

schema = graphene.Schema(query=Query)

# Agregar la ruta GraphQL a la aplicación Flask
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(port=4000)
