from django import forms
from django.core.exceptions import ValidationError

from home.models import Relay


class CreateRelayForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    mac_addr = forms.CharField(label='Mac Address', max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    state = forms.BooleanField(required=False, label='State', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}
    ))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateRelayForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        mac_addr = self.cleaned_data.get('mac_addr')
        user = self.request.user
        name = self.cleaned_data.get('name')
        print(user, name, "a")
        mac_addr_exists = Relay.objects.filter(mac_addr=mac_addr).exists()
        name_exists = Relay.objects.filter(name=name, user=user).exists()
        print(name_exists)
        if mac_addr_exists:
            # raise ValidationError("این آدرس مک تکراری می باشد")
            self.add_error('mac_addr', 'این آدرس مک تکراری می باشد')
        if name_exists:
            # raise ValidationError("شما قبلا از این اسم استفاده کردید")
            self.add_error('name', 'شما قبلا از این اسم استفاده کردید')
        return cleaned_data

    # def clean_mac_addr(self):
    #     mac_addr = self.cleaned_data.get('mac_addr')
    #     mac_addr_exists = Relay.objects.filter(mac_addr=mac_addr).exists()
    #     if mac_addr_exists:
    #         raise ValidationError("این آدرس مک تکراری می باشد")
    #     return mac_addr
    #
    # def clean_name(self):
    #     name = self.cleaned_data.get('name')
    #     name_exists = Relay.objects.filter(name=name).exists()
    #     if name_exists:
    #         raise ValidationError("شما قبلا از این اسم استفاده کردید")
    #     return name

class EditRelayForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    mac_addr = forms.CharField(label='Mac Address', max_length=12, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    state = forms.BooleanField(required=False, label='State', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}
    ))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditRelayForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        mac_addr = self.cleaned_data.get('mac_addr')
        user = self.request.user
        name = self.cleaned_data.get('name')
        print(user, name, "a")
        mac_addr_exists = Relay.objects.filter(mac_addr=mac_addr).exists()
        name_exists = Relay.objects.filter(name=name, user=user).exists()
        print(name_exists)
        if mac_addr_exists:
            # raise ValidationError("این آدرس مک تکراری می باشد")
            self.add_error('mac_addr', 'این آدرس مک تکراری می باشد')
        if name_exists:
            # raise ValidationError("شما قبلا از این اسم استفاده کردید")
            self.add_error('name', 'شما قبلا از این اسم استفاده کردید')
        return cleaned_data