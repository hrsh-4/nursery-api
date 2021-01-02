from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from django import forms
class PlantsCreateGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = '__all__'

class PlantsDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Plants
		fields = ['name',"description","price","image"]


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username','password','email']


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = "__all__"


class NurseryOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ['__all__']

