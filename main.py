# main.py

import multiprocessing
import subprocess

def run_graphql():
    subprocess.run(["python", "backend/graph_get_info.py"])

def run_alert_endpoint():
    subprocess.run(["python", "backend/alert_endpoint.py"])

def run_metrics():
    subprocess.run(["python", "backend/metrics.py"])

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_graphql)
    p2 = multiprocessing.Process(target=run_alert_endpoint)
    p3 = multiprocessing.Process(target=run_metrics)
    
    p1.start()
    p2.start()
    p3.start()
    
    p1.join()
    p2.join()
    p3.join()
