# Archivo: 5_anomalias.py
import xarray as xr
import matplotlib.pyplot as plt

def analizar_anomalias():
    print("Cargando datos y calculando el Balance Total (Qt)...")
    import zipfile
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
    ds['Qt'] = ds['ssr'] + ds['str'] + ds['sshf'] + ds['slhf']
    if 'valid_time' in ds.coords:
        ds = ds.rename({'valid_time': 'time'})
    
    # Promediar espacialmente para la zona de estudio
    ts_ds = ds.mean(dim=['latitude', 'longitude'])
    
    print("Calculando el ciclo climatológico base...")
    # Agrupamos por mes y promediamos (La 'normalidad')
    climatologia = ts_ds.groupby('time.month').mean('time')
    
    print("Extrayendo anomalías...")
    # A la serie original le restamos su 'normalidad' correspondiente
    anomalias = ts_ds.groupby('time.month') - climatologia
    
    # --- VISUALIZACIÓN DE ANOMALÍAS ---
    fig, ax = plt.subplots(figsize=(14, 5))
    
    # Graficar la línea de anomalía
    anomalias['Qt'].plot(ax=ax, color='black', linewidth=1)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
    
    # Rellenar de rojo las anomalías positivas (Calentamiento anómalo)
    ax.fill_between(anomalias.time.values, 0, anomalias['Qt'].values, 
                    where=(anomalias['Qt'].values > 0), 
                    color='red', alpha=0.5, label='Retención Anómala de Calor')
    
    # Rellenar de azul las anomalías negativas (Enfriamiento anómalo)
    ax.fill_between(anomalias.time.values, 0, anomalias['Qt'].values, 
                    where=(anomalias['Qt'].values < 0), 
                    color='blue', alpha=0.5, label='Pérdida Anómala de Calor')
    
    ax.set_title('Anomalías del Balance de Calor ($Q_T$) en la Costa de Valdivia')
    ax.set_ylabel('Anomalía de Energía ($J/m^2$)')
    ax.set_xlabel('Fecha')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analizar_anomalias()