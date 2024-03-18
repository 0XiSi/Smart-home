from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserSignupForm

def signin_page(request):
    next = request.GET.get('next')
    if request.user.is_authenticated:
        return redirect('home:home_page')
    signin_form = UserLoginForm()
    if request.method == 'POST':
        signin_form = UserLoginForm(data=request.POST, files=request.FILES)
        if signin_form.is_valid():

            # Login User with given Data. Data dict = form.cleaned_data
            username = signin_form.cleaned_data.get('username')
            password = signin_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect('home:home_page')
            else:
                signin_form.add_error('password', 'Username or Password is not valid')

    context = {'signin_form': signin_form}
    return render(request, 'accounts/user_signin.html', context)

def signout_page(request):
    if not request.user.is_authenticated:
        return redirect('home:home_page')
    logout(request)
    return redirect('home:home_page')

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home:home_page')
    signup_form = UserSignupForm()
    if request.method == 'POST':
        signup_form = UserSignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get('username')
            full_name = signup_form.cleaned_data.get('full_name')
            email = signup_form.cleaned_data.get('email')
            password_2 = signup_form.cleaned_data.get('password_2')
            user = User.objects.create_user(username=username, password=password_2)
            user.first_name = full_name
            user.email = email
            user.save()
            return redirect('accounts:user_signin')
    context = {'signup_form': signup_form}
    return render(request, 'accounts/user_signup.html', context)
