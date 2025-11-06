from django.urls import path
from .views import contact_message

urlpatterns = [
    path("api/contact/", contact_message, name="contact_message"),
]
