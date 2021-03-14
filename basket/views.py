from django.shortcuts import render

# Create your views here.

import json
import traceback
from basket.models import Trade, Portfolio
from basket.serializers import TradeSerializer, PortfolioSerializer
from basket.helpers import validate_trade, execute_trade, update_portfolio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict


class TradeList(APIView):
    """
    List all trades, or create a new trade.
    """
    serializer_class = TradeSerializer
    def get(self, request, format=None):
        trades = Trade.objects.all()
        serializer = TradeSerializer(trades, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        trade_obj = json.loads(json.dumps(request.data))
        try:
            validate_trade(trade_obj)
            trade_obj = execute_trade(trade_obj)
            update_portfolio(trade_obj) #make this async
        except Exception as e:
            print(traceback.format_exc())
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(model_to_dict(trade_obj), status=status.HTTP_201_CREATED)
 

class PortfolioList(APIView):
    """
    List all portfolios
    """
    def get(self, request, format=None):
        portfolio = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolio, many=True)
        return Response(serializer.data)