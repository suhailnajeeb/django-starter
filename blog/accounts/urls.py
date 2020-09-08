from django.urls import path

from .views import SignUpView

urlpatterns = [
    path('signup/', SingUpView.as_view(), name = 'signup'),
]