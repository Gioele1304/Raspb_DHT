import time
import board
import adafruit_dht

# Cablaggio del sensore DHT
sensor = adafruit_dht.DHT11(board.D4)

while True:

# acquisizione del sensore
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity

        #stampa dei valori letti, formattati con max 1 cifre decimale
        print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature, humidity))

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(2)
