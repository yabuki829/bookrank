from django.urls import path
from . import views



urlpatterns = [
    path('ranking', views.APIView.as_view(), name='index'),
]