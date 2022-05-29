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