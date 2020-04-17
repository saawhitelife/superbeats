from django.shortcuts import render, redirect
from django.http import HttpResponse
from beats.models import Beat, BeatList

# Create your views here.
def home_page(request):
        return render(request, 'home.html')

def beat_list(request):
    beats = Beat.objects.all()
    return render(request, 'beats.html', {'beats': beats})

def new_beat_list(request):
    beat_list = BeatList.objects.create()
    Beat.objects.create(title=request.POST['beat_title'], beat_list=beat_list)
    return redirect('/beats/the-unique-url/')