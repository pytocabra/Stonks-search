from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Like
from .forms import UserRegisterForm


def index(request):
    return render(request, 'search/index.html', {})

def liked(request):
    context = {
        'objects': Like.objects.all()
    }
    return render(request, 'search/user_likes.html', context)

def login(request):
    return

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created successfully!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'search/register.html', {'form': form})