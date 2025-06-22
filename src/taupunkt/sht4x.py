# Minimaler Treiber für SHT4x – SHT40/41
# Quelle: Adafruit/CircuitPython portiert für MicroPython
# Vervollständigt und erweitert um Fehlerbehandlung, CRC-Prüfung und Dokumentation

import time

class SHT4x:
    def __init__(self, i2c, address=0x44):
        """
        Initialisiert den SHT4x-Sensor.
        :param i2c: I2C-Objekt
        :param address: I2C-Adresse (Standard: 0x44)
        """
        self.i2c = i2c
        self.addr = address

    def _crc8(self, data):
        """
        Berechnet den CRC8 nach Sensirion-Standard für 2 Bytes.
        :param data: Bytes (2 Byte)
        :return: CRC8-Wert
        """
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x31
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc

    def _read_data(self, command, delay=0.01):
        """
        Sendet ein Kommando und liest 6 Bytes (2x Messwert + CRC je Wert).
        :param command: Bytestring mit Kommando
        :param delay: Wartezeit nach Kommando
        :return: (temp_raw, hum_raw) oder None bei Fehler
        """
        try:
            self.i2c.writeto(self.addr, command)
            time.sleep(delay)
            data = self.i2c.readfrom(self.addr, 6)
            if self._crc8(data[0:2]) != data[2] or self._crc8(data[3:5]) != data[5]:
                raise ValueError('CRC-Fehler bei Sensordaten')
            temp_raw = data[0] << 8 | data[1]
            hum_raw = data[3] << 8 | data[4]
            return temp_raw, hum_raw
        except Exception as e:
            print('Fehler beim Lesen vom SHT4x:', e)
            return None, None

    def measurements(self, precision='high'):
        """
        Führt eine Einzelmessung durch und gibt Temperatur und Feuchte zurück.
        :param precision: 'high', 'medium', 'low'
        :return: (Temperatur [°C], rel. Feuchte [%])
        """
        commands = {
            'high': b'\xFD',    # Single shot high precision
            'medium': b'\xF6',  # Single shot medium precision
            'low': b'\xE0',     # Single shot low precision
        }
        cmd = commands.get(precision, b'\xFD')
        temp_raw, hum_raw = self._read_data(cmd)
        if temp_raw is None:
            return None, None
        temp = -45 + (175 * (temp_raw / 65535.0))
        hum = 100 * (hum_raw / 65535.0)
        return temp, hum

    def temperature(self, precision='high'):
        """
        Gibt nur die Temperatur zurück.
        :param precision: 'high', 'medium', 'low'
        :return: Temperatur [°C] oder None
        """
        temp, _ = self.measurements(precision)
        return temp

    def relative_humidity(self, precision='high'):
        """
        Gibt nur die relative Feuchte zurück.
        :param precision: 'high', 'medium', 'low'
        :return: rel. Feuchte [%] oder None
        """
        _, hum = self.measurements(precision)
        return hum

    def pressure(self):
        """
        Dummy-Methode: SHT4x hat keinen Drucksensor.
        :return: Standard-Luftdruck [hPa]
        """
        return 1013.25

    def reset(self):
        """
        Führt einen Hard-Reset durch.
        """
        try:
            self.i2c.writeto(self.addr, b'\x94')
        except Exception as e:
            print('Fehler beim Reset:', e)

    def soft_reset(self):
        """
        Führt einen Soft-Reset durch.
        """
        try:
            self.i2c.writeto(self.addr, b'\x94')
            time.sleep(0.01)
        except Exception as e:
            print('Fehler beim Soft-Reset:', e)

    def read_serial(self):
        """
        Liest die Seriennummer des Sensors aus.
        :return: Seriennummer als Hex-String
        """
        try:
            self.i2c.writeto(self.addr, b'\x89')
            time.sleep(0.01)
            serial_data = self.i2c.readfrom(self.addr, 6)
            # CRC-Prüfung für beide 2-Byte-Blöcke
            if self._crc8(serial_data[0:2]) != serial_data[2] or self._crc8(serial_data[3:5]) != serial_data[5]:
                raise ValueError('CRC-Fehler bei Seriennummer')
            return ''.join(f'{byte:02X}' for byte in serial_data)
        except Exception as e:
            print('Fehler beim Auslesen der Seriennummer:', e)
            return None
