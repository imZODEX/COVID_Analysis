from django.urls import path
from . import views

app_name="admins"
urlpatterns = [
    path('', views.index,name="index"),
    path('reset', views.reset, name="reset"),
    path('wall', views.wall , name="wall"),
    path('accepted/',views.accept_request, name='accept_request'),
    path('approvalpage', views.approvalpage, name="approvalpage"),
    path('state/<state>', views.state, name="state"),
    path('uploaddata', views.uploaddata, name="uploaddata"),
    path('accepted/',views.accept_request, name='accept_request'),
    path('declined/',views.decline_request, name='decline_request'),
]