from django.shortcuts import render, redirect
import threading
from .models import *
from jobborse.main import run
import threading

def home(request):
    return render(request, 'jobborse/home.html', context={'tasks': Task.objects.all().order_by('-id')})

def upload_input(request):
    file = request.FILES.get('csv-file')
    if not file:
        return redirect('home')
    task = Task.objects.create(input_file=file)
    threading.Thread(target=run, args=(task,)).start()
    return redirect('home')

def download_result(request):
    pass