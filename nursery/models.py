from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.urls import reverse

class Customer(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	contact = models.PositiveIntegerField()
	
	def __str__(self):
		return self.name

class Nursery(models.Model):
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	street = models.CharField(max_length = 100)
	city = models.CharField(max_length = 100)
	contact = models.PositiveIntegerField()

	def __str__(self):
		return self.name


class Plants(models.Model):
	nursery = models.ForeignKey(Nursery, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 500)
	image = models.ImageField(upload_to = "../media/images/", blank = True, null = True, default = "../media/images/no_image.jpg")
	price = models.FloatField()

	def order_plant(self):
		return reverse('place-order', kwargs={
                    'pk':self.pk
        })

	def __str__(self):
		return self.name  +  self.nursery.name



class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
	plant = models.ForeignKey(Plants, on_delete = models.PROTECT)
	street = models.CharField(max_length = 100)
	city = models.CharField(max_length = 100)
	contact = models.PositiveIntegerField()

	

	def __str__(self):
		return f" '{self.customer.name}' , '{self.plant.name}' , '{self.plant.nursery.name}' "