from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.login),
    path('create_account', views.create_account),
    path('logout', views.logout),
    path('travels/add', views.add),
    path('add_travel', views.add_travel),
    path('travels/destination/<int:trip_id>', views.travels),
    path('delete/<int:trip_id>', views.delete),
    path('cancel/<int:trip_id>', views.cancel),
    path('join/<int:trip_id>', views.join),
]