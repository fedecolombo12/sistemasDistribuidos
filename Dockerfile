# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requerimientos en el contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido de la aplicación en el contenedor
COPY . .

# Asegúrate de que el script tenga permisos de ejecución
RUN chmod +x /app/run_all.sh

# Comando por defecto para ejecutar los scripts de Python



CMD ["/app/run_all.sh"]
