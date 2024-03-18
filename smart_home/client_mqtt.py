import paho.mqtt.client as mqtt


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('django/mqtt')
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('', '')
    client.connect(
        host='t0c2aec5.ala.asia-southeast1.emqxsl.com',
        port=8883,
        keepalive=60
    )
