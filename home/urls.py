from django.urls import path
from .views import home_page, save_relay_state, relay_list, toggle_state, get_states, create_relay, delete_relay, \
    edit_relay

app_name = 'home'
urlpatterns = [
    path('', home_page, name='home_page'),
    path('relay_list/', relay_list, name='relay_list'),
    path('save_relay_state/', save_relay_state, name='save_relay_state'),
    path('toggle_state/<str:mac_addr>/', toggle_state, name='toggle_state'),
    path('get_states/<str:mac_addr>/', get_states, name='get_relay_states'),
    path('create_relay/', create_relay, name='create_relay'),
    path('delete_relay/<str:mac_addr>', delete_relay, name='delete_relay'),
    path('edit_relay/<str:mac_addr>/', edit_relay, name='edit_relay')
,
]
