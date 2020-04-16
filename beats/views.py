from django.shortcuts import render, redirect
from django.http import HttpResponse
from beats.models import Beat

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        Beat.objects.create(title=request.POST['beat_title'])
        return redirect('/beats/the-unique-url/')
    else:
        return render(request, 'home.html')

def beat_list(request):
    beats = Beat.objects.all()
    return render(request, 'beats.html', {'beats': beats})