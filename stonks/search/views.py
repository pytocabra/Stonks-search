from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Like
from .forms import UserRegisterForm


def index(request):
    """The main view with a search bar."""
    if request.method == 'POST':
        ticker = request.POST.get('search')  # get value of the search bar
        if ticker:
            return redirect('detail', ticker=str(ticker))
    return render(request, 'search/index.html')


def detail(request, ticker):
    """The detail view with a chart and news."""
    # TODO: logic to handle yahoo api and pass data to context
    context = {
        'ticker': ticker,
    }
    return render(request, 'search/detail.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'search/register.html', {'form': form})


@login_required
def liked(request):
    """The view with liked stocks. Only for logged in users."""
    context = {
        'objects': Like.objects.filter(author=request.user.pk)
    }
    return render(request, 'search/user_likes.html', context)

