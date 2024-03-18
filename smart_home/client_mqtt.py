import paho.mqtt.client as paho
from paho import mqtt
import threading
from queue import Queue

# Queue to communicate between MQTT thread and Django views
mqtt_message_queue = Queue()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    client.subscribe("esp8266_data")

def on_message(client, userdata, msg):
    print("Received a message from topic: " + msg.topic)
    print("Message payload: " + str(msg.payload))
    # Put the received message into the queue
    mqtt_message_queue.put(msg.payload)

def mqtt_client_thread():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5,
                         callback_api_version=mqtt.client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("hivemq.webclient.1710770407588", "%C,H0BWgnF5he<2vd6M.")
    client.connect("85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud", 8883)
    client.loop_forever()