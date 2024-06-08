async function fetchGraphQLData() {
    const sensorId = document.getElementById('sensorIdInput').value;
    const query = `
        query {
            getSensorData(sensorId: ${sensorId}) {
                sensorId
                soilMoisture
                airTemperature
            }
        }
    `;
    
    try {
        const response = await fetch('http://localhost:4000/graphql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        if (result.errors) {
            throw new Error(`GraphQL error: ${result.errors.map(error => error.message).join(', ')}`);
        }

        const sensorData = result.data.getSensorData;
        
        if (sensorData) {
            const soilMoisture = parseFloat(sensorData.soilMoisture).toFixed(1);
            const airTemperature = parseFloat(sensorData.airTemperature).toFixed(1);
            document.getElementById('graphqlResult').innerText = `Sensor ID: ${sensorData.sensorId}, Soil Moisture: ${soilMoisture}% (VWC), Air Temperature: ${airTemperature}°C`;
        } else {
            document.getElementById('graphqlResult').innerText = "No data found for the specified sensor ID.";
        }
    } catch (error) {
        console.error('Error fetching GraphQL data:', error);
        document.getElementById('graphqlResult').innerText = `Error fetching data: ${error.message}`;
    }
}

// WebSocket para recibir notificaciones
document.addEventListener('DOMContentLoaded', () => {
    const socket = io('http://localhost:5000');  // Conectarse al servidor de Flask-SocketIO

    socket.on('new_alert', function(data) {
        if (data.type === 'air_temperature') {
        const message = `Nueva alerta: Sensor ID: ${data.sensor_id}, Tipo: Temperatura, Valor: ${data.value}`;
        addAlertToList(message);
        } else if (data.type === 'soil_moisture') {
        const message = `Nueva alerta: Sensor ID: ${data.sensor_id}, Tipo: Humedad del suelo, Valor: ${data.value}`;
        addAlertToList(message);
        }});
});

function addAlertToList(message) {
    const alertList = document.getElementById('alertList');
    const alertItem = document.createElement('li');
    alertItem.textContent = message;
    alertList.appendChild(alertItem);
}
