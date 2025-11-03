from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/analyze/', views.analyze, name='analyze'),
]
