from django.shortcuts import render

# Create your views here.

from django.http import * 
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Customer, Nursery, Plants, Order

from .forms import *


from rest_framework import generics, mixins
from .serializers import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.permissions import BasePermission

from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

import json



"""
		API's for
			Add a plant (nursery) (with image, price, name)
			List all plants (user)
			View a plant (user)
			Place order (user)
			View orders (nursery)

"""

class IsNursery(BasePermission):
   
	def has_permission(self, request, view):
		if Nursery.objects.filter(user = request.user):
			return True
		return False

class IsCustomer(BasePermission):
   
	def has_permission(self, request, view):
		if Customer.objects.filter(user = request.user):
			return True
		return False


class PlantsListAPI(generics.ListAPIView):
	queryset = Plants.objects.all()
	serializer_class = PlantsCreateGetSerializer



@api_view(['GET'])
def get_plant(request, pk):
	try:
		plant = Plants.objects.get(pk=pk)
	except Plants.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
 

	# get details of a single plant
	if request.method == 'GET':
		serializer = PlantsCreateGetSerializer(plant)
		return Response(serializer.data)

	

@api_view(['GET', 'POST'])
@permission_classes([IsNursery,])
def get_post_plants(request):
	# get all plants
	if request.method == 'GET':
		plants = Plants.objects.all()
		serializer = PlantsCreateGetSerializer(plants, many=True)
		return Response(serializer.data)

	# insert a new record for a plant
	if request.method == 'POST':
		nursery = Nursery.objects.filter(user = request.user)[0]
		data = {
			'name': request.data.get('name'),
			'description': request.data.get("description"),
			'image': request.data.get('image'),
			'price': request.data.get('price'),
			"nursery" : nursery.id
		}
		serializer = PlantsCreateGetSerializer(data=data)
		if serializer.is_valid():
			
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPostCustomerOrderAPI(generics.GenericAPIView):
	serializer_class = OrderSerializer
	# queryset = Order.objects.filter(customer = Customer.objects.filter(user = request.user))

	def get_queryset(self,*args,**kwargs):
		if Customer.objects.filter(user = self.request.user):
			customer = Customer.objects.filter(user = self.request.user)[0]
			orders = Order.objects.filter(customer = customer)

			queryset = orders

			return queryset

	def get(self,*args, **kwargs):
		# customer = [0]
		if Customer.objects.filter(user = self.request.user):
			customer = Customer.objects.filter(user = self.request.user)[0]
			orders = Order.objects.filter(customer = customer)
			if orders:
				queryset = orders
				serializer = OrderSerializer(queryset, many = True)
				return Response(serializer.data)
		return Response({})
	def post(self,*args, **kwargs):
		if Customer.objects.filter(user = self.request.user):
			customer = Customer.objects.get(user = self.request.user)
			print(self.request.data)
			data = self.request.data
			if data['customer'][0] != str(customer.id):
				return HttpResponse("Cant order for another user")
			serializer = OrderSerializer(data=data)
			if serializer.is_valid():
			
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return HttpResponse("Not authorised")


class NurseryOrderList(mixins.ListModelMixin,generics.GenericAPIView):
	# get all plants

	serializer_class = OrderSerializer
	
	permission_classes = [IsNursery,]


	def get_queryset(self,*args,**kwargs):
		nursery = Nursery.objects.get(user = self.request.user)
		plants= Plants.objects.filter(nursery = nursery)
		orders = []
		orders = Order.objects.filter(plant_id__in =[plant for plant in plants if Order.objects.filter(plant = plant) ] )
		# orders.append(order)
		queryset = orders
		return orders

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)





"""
	Views for  :

		login / logout 
		customer registration
		nursery registration
		list of plants
		place order



"""




def plant_list(request):
	plants = Plants.objects.all()
	print("fetching data")
	is_nursery = False
	if request.user.is_authenticated:
		if Nursery.objects.filter(user = request.user):
			is_nursery = True

	return render(request,"plant_list.html",{"plants" : plants,"is_nursery" : is_nursery})


def customer_registration(request):

	registered = False
	if request.method == 'POST':
		user_form = UserForm(request.POST, request.FILES)
		customer_form = CustomerForm(data=request.POST)
		if user_form.is_valid() and customer_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			customer = customer_form.save(commit=False)
			customer.user = user
			if not (customer_form.errors or user_form.errors):

				customer.save()
			registered = True
		else:
			print(user_form.errors,customer_form.errors)
	else:
		user_form = UserForm()
		customer_form = CustomerForm()
	return render(request,'customer_registration.html',
						  {'user_form':user_form,
						   'customer_form':customer_form,
						   'registered':registered})


def nursery_registration(request):

	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		nursery_form = NurseryForm(data=request.POST)
		if user_form.is_valid() and nursery_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			nursery = nursery_form.save(commit=False)
			nursery.user = user
			if not (user_form.errors or nursery_form.errors):

				nursery.save()
			registered = True
		else:
			print(user_form.errors,nursery_form.errors)
	else:
		user_form = UserForm()
		nursery_form = NurseryForm()
	return render(request,'nursery_registration.html',
						  {'user_form':user_form,
						   'nursery_form':nursery_form,
						   'registered':registered})


def user_login(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('home'))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'login.html', {})


@login_required(login_url='login')
def user_logout(request):

	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login')
@permission_classes((IsCustomer,))
def place_order(request,pk):
	ordered = False
	order = None
	if request.method == "POST":
		order_form = OrderForm(data = request.POST)
		if order_form.is_valid():
			order = order_form.save(commit = False)
			order.customer = Customer.objects.get(user = request.user)
			order.plant = Plants.objects.get(pk = pk)
			order.save()
			ordered = True
			return HttpResponseRedirect(reverse('home'))
		else:
			print(order_form.errors)
	else:
		if Customer.objects.filter(user = request.user):
			order_form  = OrderForm()
			return render(request,"order.html",{"order_form":order_form,"ordered"  : ordered,"order" :order})
		else:
			return HttpResponse("not a customer, placing order not allowed")


@login_required(login_url='login')
def orders(request):
	if Customer.objects.filter(user = request.user):
		customer = Customer.objects.get(user = request.user)
		orders = Order.objects.filter(customer = customer)

		return render(request,"customer_orders.html",{"orders" : orders})

	if Nursery.objects.filter(user = request.user):
		nursery = Nursery.objects.get(user = request.user)
		plants= Plants.objects.filter(nursery = nursery)
		orders = []
		orders = Order.objects.filter(plant_id__in =[plant for plant in plants if Order.objects.filter(plant = plant) ] )


		return render(request,"nursery_orders.html",{"orders" : orders})

	return HttpResponse("Not authorised ")


@login_required(login_url='login')
def add_plant(request):
	if Nursery.objects.filter(user = request.user):
		if request.method == "POST":
			plant_form = PlantForm(request.POST)
			if plant_form.is_valid():
				nursery = Nursery.objects.get(user = request.user)
				plant = Plants()
				plant.name = plant_form.cleaned_data['name']
				plant.description = plant_form.cleaned_data['description']
				plant.price = plant_form.cleaned_data['price']
				plant.image = plant_form.cleaned_data['image']

				plant.nursery = nursery
				plant.save()
				return HttpResponseRedirect(reverse("home"))
			else:
				print(plant_form.errors)
		else:
			plant_form = PlantForm()

			return render(request,"add_plant.html",{"plant_form":plant_form})
	else:
		HttpResponse("Only nursery is authorised to add plants")










# {
# 	"plant" : "hibiscus",
# 	"street" : "vijay nagar",
# 	"city" : "indore",
# 	"contact" : "78878788776"
# }