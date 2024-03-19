from django.template.defaulttags import url
from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path('ws/relay_updates/', consumers.RelayStateConsumer.as_asgi()),
    re_path(r'^ws/relay_updates/$', consumers.RelayStateConsumer.as_asgi()),
    # url(r'^ws/relay_updates/$', consumers.RelayStateConsumer.as_asgi()),
]
