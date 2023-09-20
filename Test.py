import bme680
import time
import datetime
import mh_z19
import serial  # Importieren Sie die 'serial'-Bibliothek für die Kommunikation mit MH-Z19

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Diese Oversampling-Einstellungen können angepasst werden, um das Gleichgewicht zwischen Genauigkeit und Rauschen in den Daten zu ändern.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

# Serielle Schnittstelle für MH-Z19 konfigurieren
ser = serial.Serial('/dev/serial0', baudrate=9600)  # /dev/serial0 für Raspberry Pi 3 und 4

# Polling
try:
    while True:
        if sensor.get_sensor_data():
            
            #Zeit festlegen
            varZeit = datetime.datetime.now()
            varUhrzeit = varZeit.strftime("%H:%M:%S")
            
            #Auslesen des BME680 Sensor
            varTemperatur = sensor.data.temperature
            varLuftdruck = sensor.data.pressure
            varluftfeuchtigkeit = sensor.data.humidity
            varGaswiderstand = sensor.data.gas_resistance
            
            #Auslesen des Mhz-19 Sensor
            varCo2Gehalt = mh_z19.read(ser)
            varCo2GehaltWert = varCo2Gehalt['co2']
            
            #Ausgabe der gespeicherten Werte
            print(varUhrzeit, "Temperatur: ", varTemperatur, "Grad Celsius, ","CO2-konzentration: ",varCo2GehaltWert, "ppm" , " Luftdruck: ", varLuftdruck, "hPa, ", "Luftfeuchtigkeit: ", varluftfeuchtigkeit, "%", "Gaswiderstand: ", varGaswiderstand)
            
            #Jede 1 Sekunde ausgabe der Daten
            time.sleep(1)

except KeyboardInterrupt:
    pass
