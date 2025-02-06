# Practica-N-1-Laboratorio-PDS
## Introducción  
El desarrollo de la primera práctica del laboratorio de procesamiento digital de señales tiene como objetivo la creación de un código en Python para el análisis estadístico de una señal fisiológica extraída de PhysioNet. Este análisis es importante a la hora de manipular una señal biomédica ya que permite caracterizarla y así mejorar su interpretación, lo cual es esencial para diagnósticos y monitoreos médicos.
## Señal EMG physio.net
Para el desarollo de la practica el primer paso fue buscar una señal Electromiografica obtenida por medio de physio.net con la cual pudimos extraer los archivos '.dat' y '.hea, una vez descargada la señal se importa a Python  y con la libreria "wfdb"podemos leer la señal y visualizarla para despues procesarla estadisticamente. 


```python
#finir ruta de los archivos
carpeta = r"C:\Users\alejo\Desktop\señales"
nombre_archivo = "emg_healthy"  # Sin extensión
ruta_completa = os.path.join(carpeta, nombre_archivo)

#rificar si los archivos existen
if not os.path.exists(ruta_completa + ".dat") or not os.path.exists(ruta_completa + ".hea"):
    print("Error: No se encontraron los archivos .dat y .hea en la ruta especificada.")
    exit()

#er la señal desde los archivos .dat y .hea
registro = wfdb.rdrecord(ruta_completa)
senal, info = registro.p_signal, registro.sig_name
fs = registro.fs  # Frecuencia de muestreo
```}

```
![Histograma realizado con pyton](Histograma.png)
Señal electromiografica procesada 

### Operaciones Estadisticas 
para intrpretar los datos estaditicos procedemos a realizar este analisis para esto podemos hacerlo manualmente o con "Numpy" la cual nos perminte calcular estos datos estadisticos.
```python
# Calcular estadísticas
media_np = np.mean(senal)
desvest_np = np.std(senal, ddof=1)
coef_var_np = (desvest_np / media_np) * 100

## Cálculo manual con bucles
medias_manual = []
desviaciones_manual = []
for canal in range(senal.shape[1]):  
    suma = 0
    suma_cuadrados = 0
    for i in range(len(senal)):
        suma += senal[i][canal]
    media_manual = suma / len(senal)
    medias_manual.append(media_manual)
    
    # Calcular la desviación estándar manualmente
    for i in range(len(senal)):
        suma_cuadrados += (senal[i][canal] - media_manual) ** 2
    desviacion_manual = (suma_cuadrados / (len(senal) - 1)) ** 0.5
    desviaciones_manual.append(desviacion_manual)
```}
```
Con esto obtenemos los siguentes resltados estadisticos:
![Histograma realizado con pyton](Histograma.png)

### Histograma 
```python
# Graficar histograma
    axs[1].hist(senal.flatten(), bins=50, density=True, alpha=0.6, color='b')
    axs[1].set_title("Histograma de la señal EMG")
    axs[1].set_xlabel("Amplitud")
    axs[1].set_ylabel("Frecuencia")
    axs[1].grid()

```}
```
![Histograma realizado con pyton](Histograma.jpeg)
## Relación Señal Ruido (SNR)
## Librerias 
 wfdb
 
 matplotlib.pyplot as plt

 os
 
 numpy as np

 scipy.stats as stats
 
 tkinter as tk
 
 tkinter import ttk
 
 matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

 #### 



 
