from flask import Flask
from flask_graphql import GraphQLView
import graphene
import random

app = Flask(__name__)

# Definir el tipo SensorData
class SensorData(graphene.ObjectType):
    sensor_id = graphene.Int()
    soil_moisture = graphene.Float()
    air_temperature = graphene.Float()

# Definir la consulta GraphQL
class Query(graphene.ObjectType):
    get_sensor_data = graphene.Field(SensorData, sensor_id=graphene.Int(required=True))

    def resolve_get_sensor_data(self, info, sensor_id):
        # Aquí iría tu lógica para obtener los datos del sensor desde Prometheus
        # Por ahora, generamos datos aleatorios
        return SensorData(
            sensor_id=sensor_id,
            soil_moisture=random.uniform(5, 70),
            air_temperature=random.uniform(10, 40)
        )

schema = graphene.Schema(query=Query)

# Agregar la ruta GraphQL a la aplicación Flask
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(port=4000)
