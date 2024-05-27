# main.py

import multiprocessing
import subprocess

def run_graphql():
    subprocess.run(["python", "graph_get_info.py"])

def run_alert_endpoint():
    subprocess.run(["python", "alert_endpoint.py"])

def run_metrics():
    subprocess.run(["python", "metrics.py"])

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_graphql)
    p2 = multiprocessing.Process(target=run_alert_endpoint)
    p3 = multiprocessing.Process(target=run_metrics)  # Agregar el tercer proceso para metrics.py

    p1.start()
    p2.start()
    p3.start()  # Iniciar el tercer proceso

    p1.join()
    p2.join()
    p3.join()  # Esperar a que el tercer proceso termine
