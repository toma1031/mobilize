from django.urls import path
# from .views import IndexView
from event_list import views

urlpatterns = [
    # path('', IndexView.as_view()),
    path('', views.index_view),
]