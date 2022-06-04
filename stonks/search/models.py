import imp
from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
    ticker = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200)
    date_liked = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ticker) + ' ' + str(self.date_liked)


class StockTickerData(models.Model):
    symbol = models.CharField(max_length=20)
    shortName = models.CharField(max_length=20)
    longName = models.CharField(max_length=100)
    exchange = models.CharField(max_length=20)
    market = models.CharField(max_length=20)
    quoteType = models.CharField(max_length=20)
    updateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str("Ticker {}, on market {}.".format(self.symbol, self.market))
