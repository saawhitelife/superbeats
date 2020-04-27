from django.shortcuts import render, redirect
from django.http import HttpResponse
from beats.models import Beat, BeatList
from django.core.exceptions import ValidationError


def home_page(request):
        return render(request, 'home.html')


def beat_list(request, beat_list_id):
    beat_list = BeatList.objects.get(id=beat_list_id)
    return render(request, 'beats.html', {'beat_list': beat_list})


def new_beat_list(request):
    beat_list = BeatList.objects.create()
    beat = Beat.objects.create(title=request.POST['beat_title'], beat_list=beat_list)
    try:
        beat.full_clean()
        beat.save()
    except ValidationError:
        beat_list.delete()
        error = 'You cant submit an empty beat'
        return render(request, 'home.html',
                      {'error': error})
    return redirect(f'/beat_list/{beat_list.id}/')

def add_beat(request, beat_list_id):
    beat_list = BeatList.objects.get(id=beat_list_id)
    Beat.objects.create(beat_list=beat_list, title=request.POST['beat_title'])
    return redirect(f'/beat_list/{beat_list.id}/')