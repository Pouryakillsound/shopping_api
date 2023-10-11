from django.urls import path
from .views import TestView
app_name = 'playground'


urlpatterns = [
    path('translate/', TestView.as_view(), name='translate')
]