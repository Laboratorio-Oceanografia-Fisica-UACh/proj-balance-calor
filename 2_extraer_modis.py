# 1. Asegúrese de estar dentro de la carpeta de tu proyecto
# (Ajuste la ruta si es necesario)
# cd ~/balance_calor_valdivia

# 2. Active el entorno virtual
# En la terminal: source venv/bin/activate.fish
# o .bash 

# 3. Asegúrese de que el paquete oficial de Google esté bien instalado
# pip install earthengine-api

# 4. Realizar la autenticación con earth engine
# En la terminal: earthengine authenticate

# Ejecutar el script en la terminal con: venv/bin/python 2_extraer_modis.py
import ee
import os
import requests

def extraer_sst_modis():
    print("Inicializando Earth Engine...")
    # Requiere el ID de tu proyecto de Google Cloud asociado a Earth Engine
    ee.Initialize(project='balance-calor-vald')

    # Definir la zona de interés (Polígono alrededor de Valdivia)
    # Formato: [Lon Min, Lat Min, Lon Max, Lat Max]
    roi = ee.Geometry.Rectangle([-74.0, -40.5, -73.0, -39.5])

    print("Buscando colección MODIS Aqua Nivel 3...")
    # Llamar a la colección y filtrar por fecha y zona
    dataset = (ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI')
               .filterDate('2000-01-01', '2025-01-31')
               .select('sst'))

    # Calcular el promedio temporal para ese mes y recortar a la zona
    sst_mensual = dataset.mean().clip(roi)

    print("Generando enlace de descarga para el raster (GeoTIFF)...")
    # Obtener URL de descarga directa
    url = sst_mensual.getDownloadURL({
        'scale': 4000, # Resolución en metros
        'crs': 'EPSG:4326',
        'region': roi,
        'format': 'GEO_TIFF'
    })

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    nombre_archivo = os.path.join(directorio_actual, 'modis_sst_valdivia.tif')

    print(f"Descargando imagen automáticamente... Esto puede tardar un momento.")
    respuesta = requests.get(url)
    with open(nombre_archivo, 'wb') as f:
        f.write(respuesta.content)

    print("-" * 50)
    print(f"¡Éxito! La imagen satelital se ha guardado en:\n{nombre_archivo}")
    print("-" * 50)

if __name__ == "__main__":
    extraer_sst_modis()