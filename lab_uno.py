import tkinter as tk
from tkinter import messagebox
import wfdb
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import os

# Ruta y nombre del archivo predefinidos
carpeta = r"C:\Users\alejo\Desktop\señales"
nombre_archivo = "emg_healthy"  # Sin extensión
ruta_completa = os.path.join(carpeta, nombre_archivo)

# Verificar si los archivos existen
if not os.path.exists(ruta_completa + ".dat") or not os.path.exists(ruta_completa + ".hea"):
    raise FileNotFoundError("No se encontraron los archivos .dat y .hea en la ruta especificada.")

# Leer los datos de los archivos
registro = wfdb.rdrecord(ruta_completa)
senal, info = registro.p_signal, registro.sig_name
fs = registro.fs  # Frecuencia de muestreo

# Crear eje de tiempo
tiempo = np.arange(len(senal)) / fs

# Calcular estadísticas
media_np = np.mean(senal)
desvest_np = np.std(senal, ddof=1)
coef_var_np = (desvest_np / media_np) * 100

## 2 Cálculo manual con bucles
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

# Función para calcular y mostrar SNR
def calcular_snr():
    # Generación de ruido y cálculo de SNR
    potencia_senal = np.mean(senal ** 2)
    potencia_ruido = potencia_senal / 10**(2 / 10)

    ruido_gaussiano = np.random.normal(0, np.sqrt(potencia_ruido) * 0.92, senal.shape)
    artefacto = np.zeros_like(senal)
    for i in range(senal.shape[0]):
        if np.random.rand() < 0.004:
            artefacto[i] = np.random.uniform(-1, 1) * 5
    ruido_artefacto = 4 * artefacto * np.sqrt(potencia_ruido)

    ruido_impulso = np.zeros_like(senal)
    for canal in range(senal.shape[1]):
        indices_picos = np.random.choice(len(senal), int(len(senal) * 0.01), replace=False)
        ruido_impulso[indices_picos, canal] = np.random.uniform(-1, 1, len(indices_picos))
    ruido_impulso *= np.sqrt(potencia_ruido)

    senal_gauss = senal + ruido_gaussiano
    senal_artefacto = senal + ruido_artefacto
    senal_impulso = senal + 10 * ruido_impulso

    # Función para calcular SNR individual
    def calcular_snr_individual(senal_original, senal_con_ruido):
        ruido = senal_con_ruido - senal_original
        potencia_senal = np.mean(senal_original ** 2)
        potencia_ruido = np.mean(ruido ** 2)
        return 10 * np.log10(potencia_senal / potencia_ruido)

    snr_gaussiano = calcular_snr_individual(senal, senal_gauss)
    snr_artefacto = calcular_snr_individual(senal, senal_artefacto)
    snr_impulso = calcular_snr_individual(senal, senal_impulso)

    # Mostrar los resultados de SNR
    resultados_snr = f"SNR con ruido gaussiano: {snr_gaussiano:.2f} dB\n"
    resultados_snr += f"SNR con ruido de artefacto: {snr_artefacto:.2f} dB\n"
    resultados_snr += f"SNR con ruido impulso: {snr_impulso:.2f} dB\n"
    messagebox.showinfo("Resultados SNR", resultados_snr)

    # Graficar resultados
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    axs[0, 0].plot(tiempo, senal)
    axs[0, 0].set_title("Señal Original EMG Healthy")
    axs[0, 1].plot(tiempo, senal_gauss)
    axs[0, 1].set_title(f"Ruido Gaussiano (SNR = {snr_gaussiano:.2f} dB)")
    axs[1, 0].plot(tiempo, senal_artefacto)
    axs[1, 0].set_title(f"Artefacto (SNR = {snr_artefacto:.2f} dB)")
    axs[1, 1].plot(tiempo, senal_impulso)
    axs[1, 1].set_title(f"Ruido Impulso (SNR = {snr_impulso:.2f} dB)")
    for ax in axs.flat:
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.grid()
    plt.tight_layout()
    plt.show()

# Función para mostrar las estadísticas y gráficas
def mostrar_estadisticas():
    resultados_estadisticas = f"Media (manual): {medias_manual}\n"
    resultados_estadisticas += f"Media (NumPy): {media_np}\n"
    resultados_estadisticas += f"Desviación estándar (manual): {desviaciones_manual}\n"
    resultados_estadisticas += f"Desviación estándar (NumPy): {desvest_np}\n"
    resultados_estadisticas += f"Coeficiente de variación: {coef_var_np:.2f}%\n"
    messagebox.showinfo("Resultados Estadísticas", resultados_estadisticas)

    # Gráficas de la señal original
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Graficar señal original
    axs[0].plot(tiempo, senal)
    axs[0].set_title("Señal Original EMG Healthy")
    axs[0].set_xlabel("Tiempo (s)")
    axs[0].set_ylabel("Amplitud")
    axs[0].grid()

    # Graficar histograma
    axs[1].hist(senal.flatten(), bins=50, density=True, alpha=0.6, color='b')
    axs[1].set_title("Histograma de la señal EMG")
    axs[1].set_xlabel("Amplitud")
    axs[1].set_ylabel("Frecuencia")
    axs[1].grid()

    # Graficar función de probabilidad
    valores = np.linspace(min(senal.flatten()), max(senal.flatten()), 100)
    pdf = stats.norm.pdf(valores, media_np, desvest_np)
    axs[2].plot(valores, pdf, color='r')
    axs[2].set_title("Función de Probabilidad de la señal EMG")
    axs[2].set_xlabel("Amplitud")
    axs[2].set_ylabel("Probabilidad")
    axs[2].grid()

    plt.tight_layout()
    plt.show()

# Crear la interfaz gráfica principal
root = tk.Tk()
root.title("Análisis de Señales EMG")
root.geometry("400x200")

label = tk.Label(root, text="Seleccione el análisis a realizar", font=("Arial", 14))
label.pack(pady=20)

# Botones para las opciones de análisis
boton_estadisticas = tk.Button(root, text="Estadísticas", font=("Arial", 12), command=mostrar_estadisticas)
boton_estadisticas.pack(pady=10)

boton_snr = tk.Button(root, text="SNR", font=("Arial", 12), command=calcular_snr)
boton_snr.pack(pady=10)

root.mainloop()
