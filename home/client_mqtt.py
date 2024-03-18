import paho.mqtt.client as mqtt

# MQTT broker settings
MQTT_BROKER = "85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TLS_URI = "tls://" + MQTT_BROKER + ":" + str(MQTT_PORT) + "/mqtt"

# Callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to topics upon successful connection
    client.subscribe("your_topic")

def on_message(client, userdata, msg):
    print("Received message on topic " + msg.topic + ": " + str(msg.payload))
    # Process incoming message as needed

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

# Start the MQTT client loop
mqtt_client.loop_forever()
