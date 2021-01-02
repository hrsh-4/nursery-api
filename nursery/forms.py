from django import forms
from .models import Customer, Nursery, Order, Plants
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class CustomerForm(forms.ModelForm):
	class Meta():
		model = Customer
		fields = ('name','contact')


class NurseryForm(forms.ModelForm):
	class Meta:
		model = Nursery
		fields = ('name','street','city','contact')


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['street','city','contact']

class PlantForm(forms.ModelForm):
	class Meta:
		model = Plants
		fields = ['name','description','price','image']