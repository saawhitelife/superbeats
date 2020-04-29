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
    if request.method == 'POST':
        try:
            beat = Beat(title=request.POST['beat_title'], beat_list=beat_list)
            beat.full_clean()
            beat.save()
            return redirect(beat_list)
        except ValidationError:
            error = 'You cant submit an empty beat'
    return render(request, 'beats.html', {'beat_list': beat_list,
                                          'error': error})


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
    return redirect(beat_list)