from django.urls import path
from .views import homePageView         # Update for django 3.1 - You need to use .views insted of from . import views

urlpatterns = [
    path('', homePageView, name='home'),
]