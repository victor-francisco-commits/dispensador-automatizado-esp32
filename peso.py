from machine import Pin
import time

class HX711:
    def __init__(self, dout, sck, gain=128):
        self.dout = Pin(dout, Pin.IN, pull=None)
        self.sck = Pin(sck, Pin.OUT)

        self.set_gain(gain)
        self.offset = 0
        self.scale = 1

    def set_gain(self, gain):
        if gain == 128:
            self.gain = 1
        elif gain == 64:
            self.gain = 3
        elif gain == 32:
            self.gain = 2
        else:
            self.gain = 1

        self.sck.value(0)
        self.read_raw()

    def is_ready(self):
        return self.dout.value() == 0

    def read_raw(self):
        # Esperar a que esté listo
        while not self.is_ready():
            time.sleep_us(10)

        result = 0

        # Leer 24 bits
        for _ in range(24):
            self.sck.value(1)
            time.sleep_us(1)
            result = (result << 1) | self.dout.value()
            self.sck.value(0)
            time.sleep_us(1)

        # Pulsos extra dependiendo de la ganancia
        for _ in range(self.gain):
            self.sck.value(1)
            time.sleep_us(1)
            self.sck.value(0)
            time.sleep_us(1)

        # Convertir a signed
        if result & 0x800000:
            result = result - 0x1000000

        return result

    def read_average(self, times=10):
        sum = 0
        for _ in range(times):
            sum += self.read_raw()
        return sum / times

    def tare(self, times=15):
        print("Tare...")
        self.offset = self.read_average(times)
        print("Offset:", self.offset)

    def set_scale(self, scale):
        self.scale = scale

    def get_weight(self, times=10):
        value = self.read_average(times)
        return (value - self.offset) / self.scale


# ==========================
# CONFIGURACIÓN ESP32
# ==========================

hx = HX711(dout=4, sck=5)

hx.tare()
hx.set_scale(1000)  # Ajustar después de calibrar

while True:
    peso = hx.get_weight(10)
    print("Peso:", round(peso, 2), "g")
    time.sleep(0.3)
    