import os
import cdsapi

def descargar_datos_era5():
    print("Iniciando conexión con Copernicus...")
    c = cdsapi.Client()

    # Definimos los parámetros de la solicitud
    parametros = {
        'product_type': 'reanalysis',
        'variable': [
            'surface_latent_heat_flux',
            'surface_sensible_heat_flux',
            'surface_net_solar_radiation',
            'surface_net_thermal_radiation',
            'sea_surface_temperature'
        ],
        #Seleccionamos el intervalo de tiempo de los datos.
        'year': [str(año) for año in range(2000, 2025)],
        'month': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        'day': ['01', '15'], # Días de muestra por mes
        'time': '12:00',
        'format': 'netcdf',
        'area': [-39.5, -74.0, -40.5, -73.0], # Caja para Valdivia [Norte, Oeste, Sur, Este]
    }

    # Obtenemos la ruta absoluta del directorio donde está este script
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    nombre_archivo = os.path.join(directorio_actual, 'flujos_valdivia_era5.nc')
    
    print(f"Descargando datos. Esto puede tardar unos minutos. El archivo se guardará como {nombre_archivo}")
    c.retrieve('reanalysis-era5-single-levels', parametros, nombre_archivo)
    print("¡Descarga de ERA5 completada con éxito!")

if __name__ == "__main__":
    descargar_datos_era5()