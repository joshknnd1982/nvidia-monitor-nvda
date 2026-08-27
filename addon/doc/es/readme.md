# NVIDIA Monitor

Este complemento permite realizar un seguimiento de varios parámetros de las tarjetas gráficas NVIDIA, tales como el nombre, memoria utilizada, memoria disponible y total, consumo, temperatura, entre otros.

## Atajos

Nota: Algunos parámetros de información pueden no ser compatibles o estar soportados dependiendo de la tarjeta gráfica.
Todos los siguientes atajos se pueden personalizar en los gestos de entrada/categoría NVDIAMonitor. Si se pulsan dos veces la información  se copia al portapapeles

- NVDA + alt + g: Anuncia el nombre/modelo de la GPU.
- NVDA + alt + u: Anuncia el UUID de la GPU.
- NVDA + alt + v: Anuncia la versión del driver.
- NVDA + ctrl + alt + v: Anuncia la versión de la BIOS.
- NVDA + alt + 1: Anuncia la carga de la GPU.
- NVDA + alt + 2: Anuncia la carga de la memoria.
- NVDA + alt + 3: Anuncia la memoria disponible.
- NVDA + alt + 4: Anuncia la memoria utilizada.
- NVDA + alt + 5: Anuncia la memoria total.
- NVDA + alt + 6: Anuncia la temperatura de la GPU.
- NVDA + alt + 7: Anuncia el consumo de energía.
- NVDA + alt + 8: Anuncia el límite de energía.
- NVDA + alt + 9: Anuncia la cantidad de procesos CUDA.
- NVDA + alt + 0: Anuncia la memoria utilizada por procesos.
- NVDA + ctrl + alt + 1: Anuncia la velocidad de los ventiladores.
- NVDA + ctrl + alt + 2: Anuncia la frecuencia del reloj GPU.
- NVDA + ctrl + alt + 3: Anuncia la frecuencia máxima del reloj GPU.
- NVDA + ctrl + alt + 4: Anuncia la frecuencia del reloj SM.
- NVDA + ctrl + alt + 5: Anuncia la frecuencia máxima del reloj SM.
- NVDA + ctrl + alt + 6: Anuncia la frecuencia del reloj memoria.
- NVDA + ctrl + alt + 7: Anuncia la frecuencia máxima del reloj memoria.
- NVDA + ctrl + alt + 8: Anuncia el TX Throughput.
- NVDA + ctrl + alt + 9: Anuncia el RX Throughput.
- NVDA + ctrl + alt + 0: Anuncia el estado de energía.


## Registro de cambios

### Versión 2.1.1

- Se añadió la traducción al ruso.
- Se corrigió un error por el que un mensaje podía no anunciarse en absoluto
  cuando el complemento informaba de un problema en un idioma cuyos caracteres
  no admite la página de códigos del sistema.

### Versión 2.0

- Compatibilidad con NVDA 2026.1.
- A partir de esta versión, el complemento realiza llamadas directamente a la librería pynvml en lugar de utilizar una herramienta externa, siempre que se ejecute en la última versión de NVDA.
- Traducción al inglés.

### Versión 1.0

- Se realizaron varios cambios, correcciones y mejoras en el script donde se obtiene la información.
- Ahora si se produce un error se almacena en un archivo llamado NVIDIAMonitor.log el cual se encuentra en la carpeta de configuración de NVDA.
- Compatibilidad con NVDA 2025.1
- Se reasignaron algunos atajos existentes.
- Nuevos atajos añadidos:
  - UUID de la GPU: NVDA + alt + u
  - Versión del driver: NVDA + alt + v
  - Versión de la BIOS: NVDA + ctrl + alt + v
  - Carga de la memoria: NVDA + alt + 2
  - Límite de energía: NVDA + alt + 8
  - Memoria utilizada por procesos: NVDA + alt + 0
  - Frecuencia máxima del reloj GPU: NVDA + ctrl + alt + 3
  - Frecuencia del reloj SM: NVDA + ctrl + alt + 4
  - Frecuencia máxima del reloj SM: NVDA + ctrl + alt + 5
  - Frecuencia del reloj memoria: NVDA + ctrl + alt + 6
  - Frecuencia máxima del reloj memoria: NVDA + ctrl + alt + 7
  - TX Throughput: NVDA + ctrl + alt + 8
  - RX Throughput: NVDA + ctrl + alt + 9
  - Estado de energía: NVDA + ctrl + alt + 0

### Versión 0.2

- Ahora si se pulsa un atajo dos veces copia la información al portapapeles.
- Varias mejoras y optimizaciones.

### Versión 0.1

- Versión inicial del complemento.
