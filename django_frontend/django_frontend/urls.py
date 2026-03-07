from django.urls import path
from chatapp import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/send/", views.send_message, name="send_message"),
]