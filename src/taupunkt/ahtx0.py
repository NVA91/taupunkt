# AHT20 Treiber für MicroPython (vollständig)
import time

class AHT20:
    def __init__(self, i2c, address=0x38):
        """
        Initialisiert den AHT20 Sensor und prüft, ob er bereit ist.
        """
        self.i2c = i2c
        self.addr = address
        self._init_sensor()

    def _init_sensor(self):
        # Soft-Reset
        try:
            self.i2c.writeto(self.addr, b'\xBA')
            time.sleep(0.02)
        except Exception:
            pass
        # Initialisierung
        self.i2c.writeto(self.addr, b'\xBE')
        time.sleep(0.02)
        # Kalibrierung prüfen
        for _ in range(5):
            status = self._status()
            if status & 0x08:
                return
            time.sleep(0.02)
        raise RuntimeError('AHT20 nicht kalibriert oder nicht bereit')

    def _status(self):
        try:
            return self.i2c.readfrom(self.addr, 1)[0]
        except Exception:
            return 0

    def _trigger(self):
        self.i2c.writeto(self.addr, b'\xAC\x33\x00')
        time.sleep(0.08)

    def _read(self):
        for _ in range(3):
            try:
                data = self.i2c.readfrom(self.addr, 6)
                if not (data[0] & 0x80):  # Busy-Bit prüfen
                    return data
                time.sleep(0.01)
            except Exception:
                time.sleep(0.01)
        raise RuntimeError('AHT20 Antwortfehler oder Sensor busy')

    @property
    def temperature(self):
        """
        Gibt die Temperatur in Grad Celsius zurück.
        """
        self._trigger()
        data = self._read()
        temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        return temp_raw * 200 / 1048576 - 50

    @property
    def relative_humidity(self):
        """
        Gibt die relative Luftfeuchtigkeit in Prozent zurück.
        """
        self._trigger()
        data = self._read()
        hum_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
        return hum_raw * 100 / 1048576

    def reset(self):
        """
        Führt einen Soft-Reset des Sensors durch.
        """
        self.i2c.writeto(self.addr, b'\xBA')
        time.sleep(0.02)

    def is_calibrated(self):
        """
        Prüft, ob der Sensor kalibriert ist.
        """
        return bool(self._status() & 0x08)