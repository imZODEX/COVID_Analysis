from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path('', views.index,name="index"),
    path('reset', views.reset, name="reset"),
    path('wall', views.wall , name="wall"),
]