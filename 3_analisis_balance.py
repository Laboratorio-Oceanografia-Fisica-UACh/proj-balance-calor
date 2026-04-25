# Ejecutar script en la consola con: venv/bin/python 3_analisis_balance.py

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import zipfile
import os

def analizar_balance_calor():
    print("Cargando datos de ERA5...")
    # 1. Cargar el dataset
    archivo_descargado = 'flujos_valdivia_era5.nc'
    
    # La nueva API de Copernicus descarga un ZIP cuando se mezclan variables instantáneas y acumuladas.
    if zipfile.is_zipfile(archivo_descargado):
        print("El archivo descargado es un ZIP. Extrayendo archivos NetCDF...")
        with zipfile.ZipFile(archivo_descargado, 'r') as zip_ref:
            zip_ref.extractall('era5_data')
        
        # Leemos y combinamos los dos archivos NetCDF extraídos
        ds1 = xr.open_dataset('era5_data/data_stream-oper_stepType-instant.nc')
        ds2 = xr.open_dataset('era5_data/data_stream-oper_stepType-accum.nc')
        ds = xr.merge([ds1, ds2], compat='override')
    else:
        ds = xr.open_dataset(archivo_descargado)

    # 2. Calcular el Balance de Calor Total (Qt)
    # ERA5 nombra las variables así:
    # ssr: surface_net_solar_radiation
    # str: surface_net_thermal_radiation
    # sshf: surface_sensible_heat_flux
    # slhf: surface_latent_heat_flux
    ds['Qt'] = ds['ssr'] + ds['str'] + ds['sshf'] + ds['slhf']

    # Asignar atributos para los gráficos
    ds['Qt'].attrs['long_name'] = 'Balance de Calor Superficial Total'
    ds['Qt'].attrs['units'] = 'J m**-2' # ERA5 entrega energía acumulada por defecto

    # 3. Preparar las visualizaciones en ventanas/figuras distintas

    print("Generando serie de tiempo...")
    # --- GRÁFICO 1: Serie de Tiempo (Promedio espacial) ---
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    # Promediamos sobre latitud y longitud para tener 1 solo valor por cada tiempo
    qt_serie_tiempo = ds['Qt'].mean(dim=['latitude', 'longitude'])
    
    # Graficar cada uno de los componentes y el total
    ds['ssr'].mean(dim=['latitude', 'longitude']).plot(ax=ax1, label='Onda Corta (Sol)', color='orange', alpha=0.7)
    ds['str'].mean(dim=['latitude', 'longitude']).plot(ax=ax1, label='Onda Larga (Térmica)', color='red', alpha=0.7)
    ds['slhf'].mean(dim=['latitude', 'longitude']).plot(ax=ax1, label='Calor Latente', color='blue', alpha=0.7)
    ds['sshf'].mean(dim=['latitude', 'longitude']).plot(ax=ax1, label='Calor Sensible', color='cyan', alpha=0.7)
    qt_serie_tiempo.plot(ax=ax1, label='Balance Total (Qt)', color='black', linewidth=2)

    ax1.axhline(0, color='gray', linestyle='--') # Línea del cero
    ax1.set_title('Evolución Temporal del Balance Térmico\n(Promedio zona Valdivia)')
    ax1.set_ylabel('Energía (J/m²)')
    ax1.set_xlabel('Fecha')
    ax1.legend(loc='best', fontsize='small')

    fig1.tight_layout()

    print("Generando mapa espacial...")
    # --- GRÁFICO 2: Mapa Espacial (Promedio temporal) ---
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    # Promediamos sobre el tiempo para ver el comportamiento medio de la zona
    qt_mapa = ds['Qt'].mean(dim='valid_time')
    
    # Graficar el mapa
    mapa = qt_mapa.plot(ax=ax2, cmap='RdBu_r', center=0, 
                        cbar_kwargs={'label': 'Energía Promedio (J/m²)'})
    ax2.set_title('Distribución Espacial del Balance Total (Promedio 2023)')
    ax2.set_xlabel('Longitud')
    ax2.set_ylabel('Latitud')

    fig2.tight_layout()
    plt.show()

if __name__ == "__main__":
    analizar_balance_calor()