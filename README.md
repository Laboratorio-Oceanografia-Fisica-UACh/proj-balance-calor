# Balance de Calor en la Costa de Valdivia

Este proyecto tiene como objetivo analizar el balance de calor superficial en la costa de Valdivia, Chile. Utiliza datos de reanálisis climático ERA5 (Copernicus) y datos satelitales de temperatura superficial del mar de MODIS Aqua (Google Earth Engine) para calcular, analizar y visualizar los flujos de energía oceánica y atmosférica.

## Descripción del Proyecto

El balance de calor total ($Q_T$) se calcula sumando los componentes principales del flujo de energía:
* Radiación solar neta de onda corta (`ssr`)
* Radiación térmica neta de onda larga (`str`)
* Flujo de calor latente (`slhf`)
* Flujo de calor sensible (`sshf`)

El proyecto está dividido en varios scripts secuenciales que manejan desde la descarga automatizada de los datos, el cálculo del balance, el análisis estadístico de los forzantes climáticos, hasta el estudio de anomalías temporales.

## Requisitos y Configuración

Antes de ejecutar los scripts, asegúrese de cumplir con los siguientes requisitos:

1. **Entorno de Python:** El proyecto utiliza un entorno virtual. Asegúrese de activarlo antes de ejecutar los scripts:
   ```bash
   source venv/bin/activate
   # Si usa fish shell: source venv/bin/activate.fish
   ```

2. **Copernicus Climate Data Store (CDS):**
   * Es necesario tener una cuenta en [Copernicus CDS](https://cds.climate.copernicus.eu/).
   * Debe tener configurado el archivo `.cdsapirc` en su directorio de usuario (`~/.cdsapirc`) con su URL y token de API para que el paquete `cdsapi` pueda descargar los datos.

3. **Google Earth Engine:**
   * Requiere una cuenta de Google Cloud y acceso a Google Earth Engine.
   * Se necesita autenticar la API ejecutando en la terminal:
     ```bash
     earthengine authenticate
     ```

## Descripción de los Scripts

Los scripts deben ser ejecutados en el siguiente orden:

### `1_descargar_era5.py`
Descarga datos históricos (2000-2024) de flujos de calor de superficie del reanálisis ERA5 para la región de Valdivia a través de la API de Copernicus. Los datos se guardan en un archivo NetCDF (`flujos_valdivia_era5.nc`). Dependiendo de la actualización de Copernicus, puede descargar un `.zip` que los scripts posteriores manejan automáticamente.

### `2_extraer_modis.py`
Extrae datos de Temperatura Superficial del Mar (SST) promediada del satélite MODIS Aqua utilizando Google Earth Engine para la misma región de estudio. Genera un archivo GeoTIFF llamado `modis_sst_valdivia.tif`.

### `3_analisis_balance.py`
Carga los datos NetCDF descargados, unifica las variables (instantáneas y acumuladas, si aplica) y calcula el Balance de Calor Total ($Q_T$). Genera dos visualizaciones:
* Serie de tiempo promedio de los componentes individuales de calor y del $Q_T$.
* Mapa espacial de la distribución media de energía en el área de estudio.

### `4_estadistica_forzantes.py`
Realiza un análisis estadístico para determinar qué variable influye más en el sistema:
* Calcula desviaciones estándar de los componentes.
* Genera la climatología mensual (ciclo anual) de los flujos de calor.
* Crea una matriz de correlación de Pearson para ver cómo los componentes se relacionan con el Balance Total.

### `5_anomalias.py`
Calcula la climatología base mensual y extrae las anomalías de la serie de tiempo para el balance de calor ($Q_T$). Visualiza gráficamente las áreas de retención anómala de calor (positivo, en rojo) y de pérdida anómala de calor (negativo, en azul) a lo largo de los años de estudio.

## Ejecución

Puede ejecutar cada uno de los scripts de forma individual desde la raíz del proyecto, siempre usando el intérprete del entorno virtual:

```bash
venv/bin/python 1_descargar_era5.py
venv/bin/python 2_extraer_modis.py
venv/bin/python 3_analisis_balance.py
venv/bin/python 4_estadistica_forzantes.py
venv/bin/python 5_anomalias.py
```

## Librerías principales utilizadas
* `xarray`: Manejo de datos multidimensionales (NetCDF).
* `pandas`: Análisis estadístico y manejo de series de tiempo.
* `matplotlib` / `seaborn`: Visualización y gráficos.
* `cdsapi`: Conexión con Copernicus Climate Data Store.
* `earthengine-api`: Conexión con Google Earth Engine.
