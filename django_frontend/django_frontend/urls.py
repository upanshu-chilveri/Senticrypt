from django.urls import path
from senticrypt import views

urlpatterns = [
    path("",             views.index,        name="index"),
    path("api/analyse/", views.analyse_text, name="analyse_text"),
    path("api/decrypt/", views.decrypt_text, name="decrypt_text"),
]
