from django.shortcuts import render_to_response
from eventcal.models import Event

def event_view(request):
    event_list = Event.objects.all()

