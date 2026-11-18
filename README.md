```markdown
# Dispensador Automatizado con Telemetría Web (ESP32 + MicroPython)

Sistema mecatrónico de dosificación controlada por peso y monitoreo de nivel en tiempo real, gestionado mediante un servidor web embebido en **MicroPython** sobre un microcontrolador **ESP32**.

---

## Descripción del Sistema

El prototipo automatiza la entrega precisa de porciones y supervisa el almacenamiento mediante tres subsistemas integrados:
1. **Control de dosificación por peso:** Una celda de carga acoplada al módulo conversor **HX711** mide en tiempo real la masa dispensada, deteniendo el suministro al alcanzar el gramaje objetivo configurado.
2. **Accionamiento mecánico preciso:** Un motor paso a paso (**NEMA 17**) controlado por un driver **A4988** acciona el mecanismo dosificador (tornillo sin fin / compuerta rotativa) con control exacto de pasos y velocidad.
3. **Monitoreo de nivel de tolva:** Un sensor ultrasónico **HC-SR04** calcula el porcentaje de llenado restante en el depósito y alerta cuando el nivel es bajo.
4. **Interfaz Web Embebida (Telemetría):** El ESP32 aloja una página web ligera accesible desde cualquier navegador en la red local para visualizar el peso actual, el nivel del tanque y ejecutar dispensaciones manuales o programadas.

---

## Arquitectura del Sistema

```text
[Interfaz Web (Cliente HTTP)] ◄──── Wi-Fi ────► [Servidor Web MicroPython (ESP32)]
                                                        │
                      ┌─────────────────────────────────┼─────────────────────────────────┐
                      ▼                                 ▼                                 ▼
            [Celda de Carga + HX711]          [Driver A4988 + Motor]              [Sensor HC-SR04]
             (Lectura de peso en g)           (Dosificación por pasos)            (Nivel de tolva %)

```

---

## Hardware y Pinout Referencial (ESP32)

| Componente | Pin ESP32 | Función |
| --- | --- | --- |
| **Módulo HX711 (DT / SCK)** | `GPIO 16` / `GPIO 17` | Lectura digital de celda de carga ($24\text{-bit}$) |
| **Driver A4988 (STEP / DIR)** | `GPIO 18` / `GPIO 19` | Control de pulsos y sentido del motor paso a paso |
| **Driver A4988 (ENABLE)** | `GPIO 21` | Habilitación / ahorro de energía de bobinas |
| **Sensor HC-SR04 (TRIG)** | `GPIO 5` | Disparo de pulso ultrasónico |
| **Sensor HC-SR04 (ECHO)** | `GPIO 4` | Recepción de eco (con divisor de voltaje a $3.3\text{ V}$) |

*(Nota: Verifica y ajusta los pines en `main.py` según el esquemático final de tu placa).*

---

## Estructura del Repositorio

```text
├── src/
│   ├── main.py        # Lógica principal, servidor web HTTP y control de ciclo
│   ├── hx711.py       # Driver de lectura y calibración de celda de carga
│   └── hcsr04.py      # Librería de medición de distancia por ultrasonido
├── hardware/
│   └── diagrama_conexiones.png   # Esquema eléctrico y alimentación (12V motor / 5V-3.3V lógica)
└── README.md

```

---

## Instalación y Puesta en Marcha

1. **Flashear firmware MicroPython:** Cargar el binario oficial de MicroPython para ESP32 mediante `esptool` o **Thonny IDE**.
2. **Configurar credenciales Wi-Fi:** Editar las variables `SSID` y `PASSWORD` en `src/main.py`.
3. **Calibración de balanza:** Ajustar el factor de escala (`scale_factor`) en `main.py` utilizando un peso patrón conocido.
4. **Cargar archivos al ESP32:** Subir los scripts de la carpeta `src/` a la memoria flash del microcontrolador y reiniciar la placa.
5. **Acceso remoto:** Abrir la dirección IP asignada al ESP32 desde cualquier navegador web en la misma red para operar el dispensador.

---

## Tecnologías Utilizadas

* **Firmware & Lenguaje:** MicroPython, ESP32, sockets TCP/HTTP
* **Sensores y Potencia:** Celda de carga + HX711, sensor ultrasónico HC-SR04, driver A4988, motor paso a paso NEMA 17

```

```
