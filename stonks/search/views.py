from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Like, StockTickerData
from .forms import UserRegisterForm

from .update_ticker_database import update_tickers_in_database, clear_table
from .yafi_data import get_data_for_ticker

def index(request):
    """The main view with a search bar."""

    # clear_table()
    # update_tickers_in_database()

    companies = StockTickerData.objects.values_list("longName")
    companies = [company[0] for company in companies]

    if request.method == 'POST':
        ticker = request.POST.get('search')  # get value of the search bar
        if ticker:
            return redirect('detail', ticker=str(ticker))
    return render(request, 'search/index.html', {"companies": companies})


def detail(request, ticker):
    """The detail view with a chart and news."""
    # TODO: logic to handle yahoo api and pass data to context
    ticker_name = [symbol[0] for symbol in StockTickerData.objects.filter(longName__contains=ticker).values_list("symbol")]

    data_for_max, data_for_quarter, data_for_month, news = get_data_for_ticker(ticker_name[0])
    context = {
        'ticker': ticker_name[0],
        'longName': ticker,
        'data_max': data_for_max,
        'data_for_quarter': data_for_quarter,
        'data_for_month': data_for_month,
        'news': news
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


