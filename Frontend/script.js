async function fetchGraphQLData() {
    const sensorId = document.getElementById('sensorIdInput').value;
    const query = `
        query {
            getSensorData(sensorId: ${sensorId}) {
                sensor_id
                soil_moisture
                air_temperature
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
        const result = await response.json();
        document.getElementById('graphqlResult').innerText = JSON.stringify(result, null, 2);
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
