
import network
import time
import dht
import machine
import json
from umqtt.simple import MQTTClient

# =====================================
# 1. Wi-Fi
# =====================================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Connexion au Wi-Fi...")

if not wifi.isconnected():
    wifi.connect("Wokwi-GUEST", "")

    timeout = 30
    while not wifi.isconnected() and timeout > 0:
        print(".")
        time.sleep(1)
        timeout -= 1

if not wifi.isconnected():
    raise RuntimeError("Wi-Fi connection failed")

print("Wi-Fi connecte !")
print("IP :", wifi.ifconfig()[0])


# =====================================
# 2. HiveMQ
# =====================================

HIVEMQ_SERVER = "noblemason-dd049852.a03.euc1.aws.hivemq.cloud"
HIVEMQ_PORT = 8883
HIVEMQ_USER = "esp32"
HIVEMQ_PASSWORD = "REMPLACE_PAR_TON_MOT_DE_PASSE_HIVEMQ"

HIVEMQ_TOPIC = b"plant/01/telemetry"

hivemq = MQTTClient(
    "ESP32_Plant_01",
    HIVEMQ_SERVER,
    port=HIVEMQ_PORT,
    user=HIVEMQ_USER,
    password=HIVEMQ_PASSWORD,
    ssl=True,
    ssl_params={"server_hostname": HIVEMQ_SERVER}
)


# =====================================
# 3. Adafruit IO
# =====================================

AIO_SERVER = "io.adafruit.com"
AIO_PORT = 8883
AIO_USER = "SARA48"
AIO_KEY = "REMPLACE_PAR_TON_AIO_KEY"

aio = MQTTClient(
    "ESP32_Plant_01_AIO",
    AIO_SERVER,
    port=AIO_PORT,
    user=AIO_USER,
    password=AIO_KEY,
    ssl=True,
    ssl_params={"server_hostname": AIO_SERVER}
)

TOPIC_TEMP = b"SARA48/feeds/temperature"
TOPIC_HUM = b"SARA48/feeds/humidity"
TOPIC_SOIL = b"SARA48/feeds/soil-moisture"


# =====================================
# 4. Connexion aux deux serveurs
# =====================================

print("Connexion a HiveMQ...")
hivemq.connect()
print("HiveMQ connecte !")

print("Connexion a Adafruit IO...")
aio.connect()
print("Adafruit IO connecte !")


# =====================================
# 5. Capteurs
# =====================================

# DHT22 -> GPIO 14
dht_sensor = dht.DHT22(machine.Pin(14))

# Soil Moisture -> GPIO 34
soil_sensor = machine.ADC(machine.Pin(34))


# =====================================
# 6. Boucle principale
# =====================================

while True:
    try:
        # Lire DHT22
        dht_sensor.measure()

        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # Lire l'humidite du sol
        moisture_raw = soil_sensor.read()

        moisture_percent = round(
            (moisture_raw / 4095) * 100, 1
        )

        # Creer le JSON pour HiveMQ
        data = {
            "device": "ESP32_Plant_01",
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": moisture_percent
        }

        message = json.dumps(data)

        # Envoyer le JSON a HiveMQ
        hivemq.publish(HIVEMQ_TOPIC, message.encode())

        print("JSON envoye a HiveMQ :")
        print(message)

        # Envoyer chaque mesure a son Feed Adafruit IO
        aio.publish(TOPIC_TEMP, str(temperature))
        aio.publish(TOPIC_HUM, str(humidity))
        aio.publish(TOPIC_SOIL, str(moisture_percent))

        print("Donnees envoyees a Adafruit IO !")
        print("Temperature :", temperature, "C")
        print("Humidity :", humidity, "%")
        print("Soil Moisture :", moisture_percent, "%")
        print("-----------------------------")

    except Exception as e:
        print("Erreur :", e)

    time.sleep(5)
