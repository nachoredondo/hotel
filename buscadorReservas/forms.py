from django import forms

class FormContact(forms.Form):
    asunto = forms.CharField()
    mail = forms.EmailField()
    message = forms.CharField()

class FormDateReservation(forms.Form):
    entry_date = forms.DateField()
    departure_date = forms.DateField()

class FormCreateReservation(forms.Form):
    room = forms.IntegerField()
    entry_date = forms.DateField()
    departure_date = forms.DateField()
    name = forms.CharField()
    mail = forms.EmailField()
    phone_number = forms.CharField()
    n_guest = forms.IntegerField()
           