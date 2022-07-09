

from django.db import models
from django.conf import settings

# Create your models here.


class Stock(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)

    class Meta:
        unique_together = ("user", "ticker")
        # print(unique_together)

    def __str__(self):
        return self.ticker
