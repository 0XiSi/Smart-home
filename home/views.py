import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .forms import CreateRelayForm, EditRelayForm
from .models import Relay

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
    return JsonResponse(list(relay_states), safe=False)

@login_required
def toggle_state(request, mac_addr):
    print(mac_addr)
    relay = get_object_or_404(Relay, mac_addr=mac_addr, user=request.user)
    relay.state = not relay.state
    relay.save()
    return redirect('home:relay_list')

@login_required
def delete_relay(request, mac_addr):
    relay = get_object_or_404(Relay, mac_addr=mac_addr, user=request.user)
    if relay.user != request.user:
        return redirect('home:home_page')
    relay.delete()

    return redirect('home:relay_list')
