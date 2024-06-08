#!/bin/bash
python /app/metrics.py &
python /app/alert_endpoint.py &
python /app/graph_get_info.py &
wait
