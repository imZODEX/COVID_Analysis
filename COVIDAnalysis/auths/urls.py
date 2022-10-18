from django.urls import path
from . import views

app_name="auths"
urlpatterns = [
    path('', views.index),
    path('login', views.login,name="login"),
    path('register', views.register,name="register"),
    path('reset', views.reset, name="reset"),
]
