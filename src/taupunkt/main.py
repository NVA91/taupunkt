# Taupunktsteuerung für Raspberry Pi Pico (MicroPython)
# Sensoren: SHT41 (innen), AHT20 + BMP280 (außen)
# Anzeige: ST7789 LCD (Waveshare 1.47")
# Signalisierung: Ampel-LEDs (Rot, Gelb, Grün)


import time
import math
from machine import Pin, I2C, SPI
import sht4x
import ahtx0
import bmp280
import st7789
import vga1_8x8 as font
# Optional: Für größere Schrift eine andere Font-Datei importieren, falls vorhanden
# import vga1_16x32 as font_large


# ========== KONFIGURATION ==========


# I2C Pins
I2C_SDA = 0
I2C_SCL = 1

# Sensoradressen
AHT20_ADDR = 0x38
BMP280_ADDR = 0x76
SHT41_ADDR = 0x44


# LED Pins
LED_ROT = 13
LED_GELB = 14
LED_GRUEN = 15


# LCD/ST7789 SPI Pins
LCD_CS = 17
LCD_DC = 16
LCD_RST = 20
LCD_BL = 21
SPI_SCK = 18
SPI_MOSI = 19


# LCD Maße
TFT_WIDTH = 172
TFT_HEIGHT = 320


# Prüfintervall (Sekunden)
INTERVALL = 900


# Taupunktgrenze
TAUPUNKT_GRENZE = 2.0




# ========== FARB- & LAYOUT-DEFINITIONEN ==========
# Definieren Sie hier Ihre Lieblingsfarben
FARBE_HINTERGRUND = st7789.BLACK
FARBE_TEXT = st7789.WHITE
FARBE_WERT = st7789.WHITE
FARBE_INFO = st7789.CYAN
FARBE_DRUCK = st7789.ORANGE


# Farben für den Status
STATUS_GRUEN = st7789.color(0, 100, 0) # Dunkles Grün
STATUS_GELB = st7789.color(255, 215, 0) # Gold
STATUS_ROT = st7789.color(139, 0, 0) # Dunkles Rot




# ========== INIT HARDWARE ==========


# I2C
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)


# Sensoren
sensor_innen = sht4x.SHT4x(i2c, address=SHT41_ADDR)
sensor_aussen = ahtx0.AHT20(i2c, address=AHT20_ADDR)
sensor_druck = bmp280.BMP280(i2c, addr=BMP280_ADDR)


# LEDs
led_rot = Pin(LED_ROT, Pin.OUT)
led_gelb = Pin(LED_GELB, Pin.OUT)
led_gruen = Pin(LED_GRUEN, Pin.OUT)


# Display
spi = SPI(0, baudrate=30000000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI))
tft = st7789.ST7789(
    spi, TFT_WIDTH, TFT_HEIGHT,
    reset=Pin(LCD_RST, Pin.OUT),
    dc=Pin(LCD_DC, Pin.OUT),
    cs=Pin(LCD_CS, Pin.OUT),
    rotation=3  # 270° Rotation für Waveshare 1.47" Display
)
tft.init()
Pin(LCD_BL, Pin.OUT).on()




# ========== FUNKTIONEN ==========


def zeige_dashboard(status, status_farbe, daten):
    """Zeigt ein strukturiertes Dashboard mit Farben an."""
    tft.fill(FARBE_HINTERGRUND)
    
    innen_t, innen_rh, aussen_t, aussen_rh, druck, tp_innen, tp_aussen = daten


    # --- INNENRAUM ---
    tft.text(font, "INNEN", 15, 15, FARBE_INFO)
    tft.text(font, f"Temp: {innen_t:.1f} C", 15, 35, FARBE_WERT)
    tft.text(font, f"Feuchte: {innen_rh:.1f} %", 15, 50, FARBE_WERT)
    tft.text(font, f"Taupunkt: {tp_innen:.1f} C", 15, 65, FARBE_WERT)


    # --- AUSSENBEREICH ---
    tft.text(font, "AUSSEN", 15, 100, FARBE_INFO)
    tft.text(font, f"Temp: {aussen_t:.1f} C", 15, 120, FARBE_WERT)
    tft.text(font, f"Feuchte: {aussen_rh:.1f} %", 15, 135, FARBE_WERT)
    tft.text(font, f"Taupunkt: {tp_aussen:.1f} C", 15, 150, FARBE_WERT)
    
    # --- DRUCK ---
    tft.text(font, f"Druck: {druck:.0f} hPa", 15, 175, FARBE_DRUCK)


    # --- STATUSLEISTE ---
    status_y_pos = 200
    tft.fill_rect(0, status_y_pos, TFT_WIDTH, TFT_HEIGHT - status_y_pos, status_farbe)
    
    # Text zentrieren für eine saubere Optik
    text_breite = len(status) * 8 # Breite des Fonts ist 8px
    text_x = (TFT_WIDTH - text_breite) // 2
    text_y = status_y_pos + 15
    tft.text(font, status, text_x, text_y, FARBE_TEXT)




def berechne_taupunkt(temp, rh):
    # Magnus-Formel Konstanten
    a, b = 17.27, 237.7
    alpha = ((a * temp) / (b + temp)) + math.log(rh / 100.0)
    return (b * alpha) / (a - alpha)


def schalte_leds(status):
    led_rot.off()
    led_gelb.off()
    led_gruen.off()
    if status == "rot":
        led_rot.on()
    elif status == "gelb":
        led_gelb.on()
    elif status == "gruen":
        led_gruen.on()


def hole_daten():
    try:
        innen_t, innen_rh = sensor_innen.measurements
        aussen_t = sensor_aussen.temperature
        aussen_rh = sensor_aussen.relative_humidity
        druck = sensor_druck.pressure
        
        # Plausibilitätsprüfung (optional, aber empfohlen)
        if not (-40 < innen_t < 80 and 0 <= innen_rh <= 100):
            raise ValueError("Innen-Sensor liefert ungültige Werte")
        
        return innen_t, innen_rh, aussen_t, aussen_rh, druck
    except Exception as e:
        tft.fill(STATUS_ROT)
        tft.text(font, "Sensorfehler!", 10, 10, FARBE_TEXT)
        tft.text(font, str(e), 10, 30, FARBE_TEXT)
        print("Fehler:", e)
        return None


def entscheide_lueften():
    raw_daten = hole_daten()
    if not raw_daten:
        return


    innen_t, innen_rh, aussen_t, aussen_rh, druck = raw_daten
    tp_innen = berechne_taupunkt(innen_t, innen_rh)
    tp_aussen = berechne_taupunkt(aussen_t, aussen_rh)


    status = ""
    status_farbe = FARBE_HINTERGRUND


    if tp_aussen < (tp_innen - TAUPUNKT_GRENZE):
        status = "Lueften empfohlen"
        status_farbe = STATUS_GRUEN
        schalte_leds("gruen")
    elif tp_aussen >= tp_innen:
        status = "Nicht lueften"
        status_farbe = STATUS_ROT
        schalte_leds("rot")
    else:
        status = "Bedingt lueften"
        status_farbe = STATUS_GELB
        schalte_leds("gelb")


    # Alle Daten in einem Tupel zusammenfassen für die Übergabe
    display_daten = (innen_t, innen_rh, aussen_t, aussen_rh, druck, tp_innen, tp_aussen)
    
    # Die neue Dashboard-Funktion aufrufen
    zeige_dashboard(status, status_farbe, display_daten)
    
    # Konsolenausgabe für Debugging beibehalten
    print(
        f"Innen: {innen_t:.1f}C, {innen_rh:.1f}%, TP: {tp_innen:.1f}C | "
        f"Aussen: {aussen_t:.1f}C, {aussen_rh:.1f}%, TP: {tp_aussen:.1f}C | "
        f"Status: {status}"
    )




# ========== HAUPTSCHLEIFE ==========


while True:
    entscheide_lueften()
    time.sleep(INTERVALL)