<img width="1021" height="321" alt="image" src="https://github.com/user-attachments/assets/7899c58c-806f-4835-a10b-9822ffe3d000" /># Smart-Plant-Monitoring
ESP32 project using DHT22, soil moisture sensor, MQTT, HiveMQ and Adafruit IO
 # Smart Plant Monitoring System

## Description

This project uses an ESP32 to monitor plant conditions in real time.

## Components

* ESP32
* DHT22 temperature and humidity sensor
* Soil moisture sensor

## Technologies

* MicroPython
* MQTT
* HiveMQ Cloud
* Adafruit IO
* Wokwi

## Sensors Connections

* DHT22 data pin: GPIO 14
* Soil moisture analog output: GPIO 34

## Features

* Reads temperature and air humidity.
* Measures soil moisture.
* Sends telemetry data to HiveMQ using MQTT.
* Sends individual sensor values to Adafruit IO.
* Updates readings every 5 seconds.

## Setup

1. Configure the Wi-Fi connection.
2. Add your HiveMQ credentials.
3. Add your Adafruit IO username and AIO key.
4. Upload `main.py` to the ESP32.
5. Run the project and check your Adafruit IO dashboard.

**Security:** Never publish real passwords or API keys in a public repository.

