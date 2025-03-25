import time
import board
import adafruit_dht
import requests

# Cablaggio del sensore DHT
sensor = adafruit_dht.DHT11(board.D4)

# Nostra chiave API da usare per le richieste
key = "F79HHSQCZEMGJGM5"

# Intestazioni necessarie alla richiesta POST
headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain",
}

thingspeak_url = "https://api.thingspeak.com/update"

while True:
    try:
        # acquisizione del sensore
        temperature = sensor.temperature
        humidity = sensor.humidity

        # stampa dei valori letti, formattati con max 1 cifre decimale
        print("Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature, humidity))

        # Invio della richiesta POST temperatura
        params = {"field1": temperature, "field2": humidity, "key": key}
        r = requests.post(thingspeak_url, data=params, headers=headers)

        # Debug: stampa a video del risultato della richiesta
        print("Dato inviato: Temp={0:0.1f}ºC, Humidity={1:0.1f}%".format(temperature, humidity))
        print(r)

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue

    except Exception as error:
        sensor.exit()
        raise error

    # Wait 5 seconds before fetching data again
    time.sleep(5)
