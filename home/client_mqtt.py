import json
import paho.mqtt.client as paho
from paho import mqtt
import threading
from queue import Queue
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from home.models import Relay

# Queue to communicate between MQTT thread and Django views
mqtt_message_queue = Queue()

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    client.subscribe("esp8266_data")

def on_message(client, userdata, msg):
    print("Received a message from topic: " + msg.topic)
    print("Message payload: " + str(msg.payload))

    # Extract the MAC address and state from the message payload
    data = json.loads(msg.payload)
    mac_addr = data.get('mac_addr')
    state = data.get('state')

    # Update the relay state in the database
    try:
        relay = Relay.objects.get(mac_addr=mac_addr)
        relay.state = state
        relay.save()
        print(f"Relay state updated: MAC address={mac_addr}, State={state}")

        # Notify clients of the state change via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "relay_updates",
            {"type": "relay.state.update", "mac_addr": mac_addr, "state": state}
        )
    except Relay.DoesNotExist:
        print(f"No relay found with MAC address: {mac_addr}")

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5,
                     callback_api_version=mqtt.client.CallbackAPIVersion.VERSION2)

def mqtt_client_thread():
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("hivemq.webclient.1710770407588", "%C,H0BWgnF5he<2vd6M.")
    client.connect("85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud", 8883)
    client.loop_forever()

def message_publisher():
    while True:
        message = input("Enter a message to publish: ")
        client.publish("esp8266_data", payload=message, qos=1)
        print(message)
publish_thread = threading.Thread(target=message_publisher)
publish_thread.start()
