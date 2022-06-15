from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.contrib.auth.models import User
from .models import Like, StockTickerData
from .forms import UserRegisterForm

from .update_ticker_database import update_tickers_in_database, clear_table
from .yafi_data import get_data_for_ticker, get_values_for_liked_tickers

import json


def index(request):
    """The main view with a search bar."""
    companies = StockTickerData.objects.values_list("longName")
    companies = [company[0] for company in companies]

    if request.method == 'POST':
        ticker = request.POST.get('search')  # get value of the search bar
        if ticker:
            return redirect('detail', ticker=str(ticker))
    return render(request, 'search/index.html', {"companies": companies})


def detail(request, ticker):
    """The detail view with a chart and news."""
    try:
        ticker_name = [symbol[0] for symbol in StockTickerData.objects.filter(longName=ticker).values_list("symbol")]
        if ticker_name:
            list_of_ticker_data = get_data_for_ticker(ticker_name[0])
            if request.user.username:
                is_liked = Like.objects.filter(ticker__contains=ticker_name[0], author__username__contains=request.user.username).exists()
            else:
                is_liked = False
        else:
            list_of_ticker_data = [None]

        if all(element is None for element in list_of_ticker_data):
            request.session['error'] = "Sorry! We have no data for chosen company."
            return redirect('error', ticker=str(ticker))
        else:
            context = {
                'ticker': ticker_name[0],
                'longName': ticker,
                'data_max': list_of_ticker_data[0],
                'news': list_of_ticker_data[1],
                'info': list_of_ticker_data[2],
                'holders': json.loads(list_of_ticker_data[3].reset_index().to_json(orient ='records')),
                'data_for_max_close_only': list_of_ticker_data[4],
                'liked': is_liked
            }
            return render(request, 'search/detail.html', context)
    except:
        request.session['error'] = "Sorry! Problem occured while accessing data."
        return redirect('error', ticker=str(ticker))


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
    liked_tickers = [sym[0] for sym in
                     Like.objects.filter(author__username__contains=request.user.username).values_list("ticker")]
    current_ticker_values = get_values_for_liked_tickers(liked_tickers)
    context = {
        'objects': Like.objects.filter(author=request.user.pk),
        'liked_tickers_json': current_ticker_values
    }
    return render(request, 'search/user_likes.html', context)


def error(request, ticker):
    context = {
        'ticker': ticker,
        'error_msg': request.session['error']
    }
    return render(request, 'search/error.html', context)


@login_required
def like_stock(request, ticker):
    #if request.method == "POST":
    ticker = ticker.upper()
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