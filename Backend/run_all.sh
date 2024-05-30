#!/bin/bash
python /app/backend/metrics.py &
python /app/backend/alert_endpoint.py &
python /app/backend/graph_get_info.py &
wait
