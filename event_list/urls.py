from django.urls import path
# from .views import IndexView
from event_list import views

urlpatterns = [
    path('', views.index_view, name="index"),
]