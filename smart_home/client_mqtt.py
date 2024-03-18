import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        client.subscribe('django/mqtt')
    else:
        print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

# Create a client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Set username and password if required
client.username_pw_set('', '')

# Connect to MQTT broker
client.connect(
    host='85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud',
    port=8883,
    keepalive=60
)

# Start the MQTT loop
client.loop_forever()
