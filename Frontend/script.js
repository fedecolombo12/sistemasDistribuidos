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
            document.getElementById('graphqlResult').innerText = `Sensor ID: ${sensorData.sensorId}, Soil Moisture: ${sensorData.soilMoisture}, Air Temperature: ${sensorData.airTemperature}`;
        } else {
            document.getElementById('graphqlResult').innerText = "No data found for the specified sensor ID.";
        }
    } catch (error) {
        console.error('Error fetching GraphQL data:', error);
    }
}

async function sendAlert() {
    const alertData = document.getElementById('alertDataInput').value;
    
    try {
        const response = await fetch('http://localhost:5000/alert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: alertData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.text();
        document.getElementById('restResult').innerText = result;
    } catch (error) {
        console.error('Error sending alert:', error);
    }
}

// WebSocket para recibir notificaciones
const socket = io('http://localhost:5000');

socket.on('new_alert', function(data) {
    const message = `New alert received: Sensor ID: ${data.sensor_id}, Value: ${data.value}`;
    showNotification(message);
});

function showNotification(message) {
    const notification = document.getElementById('notification');
    notification.innerText = message;
    notification.classList.add('show');
    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}
