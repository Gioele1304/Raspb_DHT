import time
import board
import adafruit_dht
import requests

# Configurazione dei sensori DHT con i rispettivi pin GPIO
sensors = [
    adafruit_dht.DHT11(board.D4),  # Sensore 1
    adafruit_dht.DHT11(board.D17), # Sensore 2
    adafruit_dht.DHT11(board.D27), # Sensore 3
    adafruit_dht.DHT11(board.D22), # Sensore 4
]

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
        # Lettura dei dati da tutti i sensori
        sensor_data = []
        for i, sensor in enumerate(sensors):
            try:
                temperature = sensor.temperature
                humidity = sensor.humidity
                sensor_data.append((temperature, humidity))
                print(f"Sensore {i+1}: Temp={temperature:0.1f}ºC, Humidity={humidity:0.1f}%")
            except RuntimeError as error:
                print(f"Errore sensore {i+1}: {error.args[0]}")
                sensor_data.append((None, None))  # Valori non validi per questo sensore

        # Preparazione dei parametri per la richiesta POST
        params = {
            "key": key,
            "field1": sensor_data[0][0],  # Temperatura sensore 1
            "field2": sensor_data[0][1],  # Umidità sensore 1
            "field3": sensor_data[1][0],  # Temperatura sensore 2
            "field4": sensor_data[1][1],  # Umidità sensore 2
            "field5": sensor_data[2][0],  # Temperatura sensore 3
            "field6": sensor_data[2][1],  # Umidità sensore 3
            "field7": sensor_data[3][0],  # Temperatura sensore 4
            "field8": sensor_data[3][1],  # Umidità sensore 4
        }

        # Invio della richiesta POST
        r = requests.post(thingspeak_url, data=params, headers=headers)

        # Debug: stampa a video del risultato della richiesta
        print("Dati inviati:")
        for i, (temp, hum) in enumerate(sensor_data):
            print(f"Sensore {i+1}: Temp={temp}, Humidity={hum}")
        print(f"Risposta: {r.status_code}, {r.text}")

    except Exception as error:
        print(f"Errore critico: {error}")
        for sensor in sensors:
            sensor.exit()
        raise error

    # Attesa prima della prossima lettura
    time.sleep(5)