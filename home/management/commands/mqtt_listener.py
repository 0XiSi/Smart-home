import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        def on_connect(client, userdata, flags, rc):
            print("Connected to MQTT broker with result code " + str(rc))
            # Subscribe to desired topics
            client.subscribe("test")  # Subscribe to the "test" topic

        def on_message(client, userdata, msg):
            print("Received message: " + msg.payload.decode())

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("localhost", 1883, 60)

        # Start the MQTT client loop
        client.loop_forever()
