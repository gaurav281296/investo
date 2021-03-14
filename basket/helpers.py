import decimal
from basket.models import Trade, Portfolio

def validate_trade(trade_data):
    trade_data["ticker_name"] = trade_data["ticker_name"].casefold()
    trade_data["trade_quantity"] = int(trade_data["trade_quantity"])
    trade_data["trade_price"] = decimal.Decimal(trade_data["trade_price"])
    trade_data["trade_type"] = trade_data["trade_type"].casefold()
    if trade_data["trade_price"] < 0.01:
        raise Exception("trade_price cannot be negative")
    if trade_data["trade_type"].casefold() not in ["b", "s"]:
        raise Exception("trade_type can only be 'S' or 'B'")
    if trade_data["trade_quantity"] < 1:
        raise Exception("trade_quantity has to be more than 0")
    if trade_data["trade_type"].casefold() == "b":
        trade_data["success"] = True
    else:
        try:
            portfolio = Portfolio.objects.get(portfolio_id=trade_data["portfolio_id"],ticker_name=trade_data["ticker_name"])
        except Portfolio.DoesNotExist:
            raise Exception("sold quantity more than holding - short selling is not supported")

        if portfolio.quantity < trade_data["trade_quantity"]:
            raise Exception("sold quantity more than holding - short selling is not supported")
            
 
def execute_trade(trade_data):
    trade = Trade(portfolio_id=trade_data["portfolio_id"],
        ticker_name=trade_data["ticker_name"],
        trade_type=trade_data["trade_type"].casefold(),
        trade_price=trade_data["trade_price"],
        trade_quantity=trade_data["trade_quantity"])
    trade.save()
    return trade

def update_portfolio(trade_data):
    try:
        portfolio = Portfolio.objects.get(portfolio_id=trade_data.portfolio_id,ticker_name=trade_data.ticker_name)
        if trade_data.trade_type == "b":
            new_quantity = portfolio.quantity + trade_data.trade_quantity
            new_avg_buy = ((portfolio.avg_buy_price*portfolio.quantity) + (trade_data.trade_quantity*trade_data.trade_price))/new_quantity
            portfolio.quantity = new_quantity
            portfolio.avg_buy_price = new_avg_buy
        else:
            portfolio.quantity -= trade_data.trade_quantity
        if portfolio.quantity > 0:
            portfolio.save()
        else:
            portfolio.delete()
    except Portfolio.DoesNotExist:
        portfolio = Portfolio(portfolio_id=trade_data.portfolio_id,
            ticker_name=trade_data.ticker_name,
            avg_buy_price=trade_data.trade_price,
            quantity=trade_data.trade_quantity)
        portfolio.save()