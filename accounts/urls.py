from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin_page, name='user_signin'),
    path('signout/', views.signout_page, name='user_signout'),
    path('signup/', views.signup_page, name='user_signup')
]
