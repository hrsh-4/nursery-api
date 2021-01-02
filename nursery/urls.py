from django.contrib import admin
from django.urls import path,include

from nursery import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [

	path("", views.plant_list ,name="home"),
	path("customer-registration", views.customer_registration, name = "customer-registration" ),
	path("nursery-registration", views.nursery_registration, name = "nursery-registration" ),
	path("login", views.user_login, name="login"),
	path("logout", views.user_logout, name="logout"),
	path("place-order/<int:pk>", views.place_order, name="place-order"),
	path("orders",views.orders, name="orders"),
	path("add-plant",views.add_plant, name="add-plant"),

	path("api/", views.PlantsListAPI.as_view()),
	path('api/plants/<int:pk>', views.get_plant),
	path("api/plants/", views.get_post_plants ),

	path("api/customer-orders", views.GetPostCustomerOrderAPI.as_view()),
  	
  	path("api/nursery-orders", views.NurseryOrderList.as_view()),



]


urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)