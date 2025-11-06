from django.urls import path
from .views import ContactCreateView

urlpatterns = [
    path('send/', ContactCreateView.as_view(), name='contact-send'),
]
