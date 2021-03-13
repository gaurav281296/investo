from django.db import models
from django.db.models import CharField
from django.db.models import IntegerField
from django.db.models import BooleanField
from django.db.models import DecimalField

from django.core.validators import MinValueValidator

from enum import Enum

class TradeType(Enum):   # A subclass of Enum
    BUY = "B"
    SELL = "S"

# Create your models here.
class Trade(models.Model):
    trade_id = models.IntegerField(primary_key=True)
    portfolio_id = models.IntegerField(null=False, blank=False)
    ticker_name = models.CharField(max_length=10, blank=False, null=False)
    trade_type = models.CharField(max_length=1, choices=[(tag, tag.value) for tag in TradeType])
    trade_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ['trade_id']