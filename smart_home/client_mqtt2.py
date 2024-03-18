import threading
import paho.mqtt.client as paho
from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish_v5(client, userdata, mid, reasonCode, properties):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# function to run the MQTT client loop in a separate thread
def mqtt_loop():
    client.loop_forever()

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5,
                     callback_api_version=mqtt.client.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("hqttt", "Aa1AAAAA")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish_v5 = on_publish_v5

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("b", qos=1)

# start the MQTT client loop in a separate thread
mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()

# loop for publishing messages
while True:
    message = input("Enter a message to publish: ")
    client.publish("b", payload=message, qos=1)