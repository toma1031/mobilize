from django.shortcuts import render

# Create your views here.
# 参考文献
# https://note.nkmk.me/python-requests-usage/
# https://ebi-works.com/django-view/
from django.views.generic import TemplateView
import requests

# Create your views here.
def index_view(request):
    url = 'https://api.mobilize.us/v1/events'
    response = requests.get(url)
    print(type(response)) 

index_view()