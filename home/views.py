import json
import threading
import paho.mqtt.client as paho
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .client_mqtt import mqtt_client_thread
from django.views.decorators.csrf import csrf_exempt
from .forms import CreateRelayForm, EditRelayForm
from .models import Relay
from paho import mqtt

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5, callback_api_version=mqtt.client.CallbackAPIVersion.VERSION2)
client.tls_set()
mqtt_thread = threading.Thread(target=mqtt_client_thread)
mqtt_thread.daemon = True
mqtt_thread.start()

@login_required
def relay_list(request):
    relays = Relay.objects.filter(user=request.user)
    context = {'relays': relays}
    return render(request, 'home/relay_list.html', context)


@login_required
def create_relay(request):
    print(f"request.user: {request.user}")
    if not request.user.is_authenticated:
        return redirect('home:home_page')
    form = CreateRelayForm(data=request.POST or None, request=request)
    if form.is_valid():
        print(form.cleaned_data)
        relay_name = form.cleaned_data.get('name')
        relay_mac_addr = form.cleaned_data.get('mac_addr')
        relay_state = form.cleaned_data.get('state')
        relay = Relay.objects.create(name=relay_name, state=relay_state, mac_addr=relay_mac_addr, user=request.user)
        print("Relay", relay.name, "Created")
        return redirect('home:relay_list')

    context = {'form': form}
    return render(request, 'home/create_relay.html', context)

def home_page(request):
    return render(request, 'index.html')

@login_required()
def edit_relay(request, mac_addr):
    relay = get_object_or_404(Relay, mac_addr=mac_addr, user_id=request.user.id)
    print(relay, "a")
    if request.method == 'GET':
        form = EditRelayForm(
            initial={'name': relay.name, 'mac_addr': relay.mac_addr,
                     'state': relay.state})
    else:
        form = EditRelayForm(data=request.POST, request=request)
        if form.is_valid():

            relay_name = form.cleaned_data.get('name')
            relay_mac_addr = form.cleaned_data.get('mac_addr')
            relay_state = form.cleaned_data.get('state')
            relay.name = relay_name
            relay.mac_addr = relay_mac_addr
            relay.is_shown = relay_state

            relay.save()
            return redirect('home:relay_list', relay.id)
    context = {'form': form, 'relay': relay}
    return render(request, 'home/edit_relay.html', context)


@csrf_exempt
def save_relay_state(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mac_addr = data.get('mac_addr')
            state = data.get('state')
            print(data)

            if mac_addr is None or state is None:
                return JsonResponse({'error': 'MAC address and state are required.'}, status=400)

            relay = get_object_or_404(Relay, mac_addr=mac_addr)
            relay.state = state
            relay.save()

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def get_states(request, mac_addr):
    print(request)
    relay_states = Relay.objects.filter(mac_addr=mac_addr).values('mac_addr', 'state')
    send_mqtt_message("esp8266_data", str(list(relay_states)[0]))
    return JsonResponse(list(relay_states), safe=False)

@login_required
def toggle_state(request, mac_addr):
    print(mac_addr)
    relay = get_object_or_404(Relay, mac_addr=mac_addr, user=request.user)
    relay.state = not relay.state
    relay.save()
    # send_mqtt_message("esp8266_data", f"{{'mac_addr': '{relay.mac_addr}', 'state': {relay.state}}}")
    message = json.dumps({"mac_addr": relay.mac_addr, "state": relay.state})
    send_mqtt_message("esp8266_data", message)
    return redirect('home:relay_list')

# @login_required
# def toggle_state(request):
    # Check if there are messages in the queue
    # if not mqtt_message_queue.empty():
    #     message = mqtt_message_queue.get()
    #     message_dict = json.loads(message.payload)
    #     # Process the message here, for example:
    #     # if 'mac_addr' in message_dict and 'state' in message_dict:
    #     mac_addr = message_dict['mac_addr']
    #     state = message_dict['state']
    #     print("Specific message received: ", message)
    #     relay = get_object_or_404(Relay, mac_addr=mac_addr, user=request.user, state=state)
    #     relay.save()
    # return redirect('home:relay_list')

@login_required
def delete_relay(request, mac_addr):
    relay = get_object_or_404(Relay, mac_addr=mac_addr, user=request.user)
    if relay.user != request.user:
        return redirect('home:home_page')
    relay.delete()

    return redirect('home:relay_list')

def send_mqtt_message(topic, message):
    # Define MQTT broker connection details
    mqtt_host = "85a4979f4e39416e9fabd326a49b02a6.s1.eu.hivemq.cloud"
    mqtt_port = 8883
    mqtt_username = "hivemq.webclient.1710770407588"
    mqtt_password = "%C,H0BWgnF5he<2vd6M."

    # Connect to the MQTT broker
    client.username_pw_set(mqtt_username, mqtt_password)
    client.connect(mqtt_host, mqtt_port)
    print(topic, message)
    client.publish(topic, message)

