# Archivo: 4_estadistica_forzantes.py
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def identificar_forzantes():
    print("Cargando y procesando datos...")
    import zipfile
    import os
    
    archivo_descargado = 'flujos_valdivia_era5.nc'
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
    
    # Calcular el Balance Total (Qt)
    ds['Qt'] = ds['ssr'] + ds['str'] + ds['sshf'] + ds['slhf']
    
    # Promediar espacialmente para tener una serie de tiempo única para Valdivia
    ts_ds = ds.mean(dim=['latitude', 'longitude'])
    
    # Convertir a un DataFrame de Pandas para análisis estadístico
    # Convertimos los nombres a algo más legible
    df = ts_ds[['ssr', 'str', 'slhf', 'sshf', 'Qt']].to_dataframe()
    df = df[['ssr', 'str', 'slhf', 'sshf', 'Qt']] # Asegurar que solo estas 5 columnas existan
    df.columns = ['Onda Corta (Sol)', 'Onda Larga (Térmica)', 'Calor Latente', 'Calor Sensible', 'Balance Total (Qt)']
    
    # --- ANÁLISIS 1: ESTADÍSTICA DESCRIPTIVA Y VARIANZA ---
    print("\n--- RESUMEN ESTADÍSTICO (Desviación Estándar) ---")
    print("La variable con mayor desviación estándar es la que más fluctúa y suele 'forzar' el sistema.")
    print(df.std().sort_values(ascending=False))
    
    # --- ANÁLISIS 2: CLIMATOLOGÍA MENSUAL (El Ciclo Anual) ---
    print("\nGenerando gráficos de Climatología y Correlación...")
    # Agrupar por mes y calcular el promedio
    df_mensual = df.groupby(df.index.month).mean()
    
    # Gráfico A: Ciclo Anual
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    df_mensual.plot(ax=ax, marker='o', linewidth=2)
    ax.axhline(0, color='black', linestyle='--', linewidth=1)
    ax.set_title('Ciclo Mensual Promedio de Flujos de Calor\n(Identificación de Estacionalidad)')
    ax.set_xlabel('Mes del Año')
    ax.set_ylabel('Energía Promedio (J/m²)')
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show(block=False)
    
    # --- ANÁLISIS 3: MATRIZ DE CORRELACIÓN ---
    # ¿Qué variable se correlaciona más con Qt?
    correlacion = df.corr()
    
    # Gráfico B: Matriz de Calor
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlacion, annot=True, cmap='coolwarm', vmin=-1, vmax=1, 
                fmt=".2f", linewidths=.5)
    plt.title('Matriz de Correlación de Pearson\n(¿Quién controla el Balance Total?)')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    identificar_forzantes()