from django.shortcuts import render, redirect
from django.http import HttpResponse
from beats.models import Beat, BeatList
from beats.forms import BeatForm
from django.core.exceptions import ValidationError


def home_page(request):
        return render(request, 'home.html', {
            'form': BeatForm()
        })


def beat_list(request, beat_list_id):
    beat_list = BeatList.objects.get(id=beat_list_id)
    error = ''
    form = BeatForm()
    if request.method == 'POST':
        form = BeatForm(data = request.POST)
        if form.is_valid():
            form.save(for_beat_list=beat_list)
            return redirect(beat_list)
    return render(request, 'beats.html', {'beat_list': beat_list,
                                          'form': form})


def new_beat_list(request):
    form = BeatForm(request.POST)
    if form.is_valid():
        beat_list = BeatList.objects.create()
        form.save(for_beat_list=beat_list)
        return redirect(beat_list)
    else:
        return render(request, 'home.html', {
            'form': form
        })