from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.contrib.auth.models import User
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
    ticker_name = [symbol[0] for symbol in StockTickerData.objects.filter(longName__contains=ticker).values_list("symbol")]
    if ticker_name:
        list_of_ticker_data = get_data_for_ticker(ticker_name[0])
        try:
            is_liked = bool(Like.objects.filter(ticker__contains=ticker_name[0]).values_list("ticker")[0])
            print(is_liked)
        except:
            is_liked = False
            print(is_liked)
    else:
        list_of_ticker_data = [None]
    if all(element is None for element in list_of_ticker_data):
        return redirect('error', ticker=str(ticker))
    else:
        context = {
            'ticker': ticker_name[0],
            'longName': ticker,
            'data_max': list_of_ticker_data[0],
            'data_for_quarter': list_of_ticker_data[1],
            'data_for_month': list_of_ticker_data[2],
            'news': list_of_ticker_data[3],
            'info': list_of_ticker_data[4],
            'holders': list_of_ticker_data[5],
            'data_for_max_close_only': list_of_ticker_data[6],
            'data_for_quarter_close_only': list_of_ticker_data[7],
            'data_for_month_close_only': list_of_ticker_data[8],
            'liked': is_liked
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


def error(request, ticker):
    error_message = "Sorry! No data for given ticker!"
    context = {
        'ticker': ticker,
        'longName': ticker,
        'error_message': error_message
    }
    return render(request, 'search/error.html', context)


@login_required
def like_stock(request, ticker):
    #if request.method == "POST":
    ticker=ticker.upper()
    object = StockTickerData.objects.filter(symbol=ticker).values()[0]
    Like(
        ticker=ticker, 
        company_name=object['longName'],
        author=User.objects.get(username=request.user.username)
        ).save()
    return redirect('liked')


@login_required
def delete_stock(request, ticker):
    #if request.method == "POST":
    ticker=ticker.upper()
    Like.objects.filter(
        ticker=ticker, 
        author__username=request.user.username).delete()
    return redirect('liked')