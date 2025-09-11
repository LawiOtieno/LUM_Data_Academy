
from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def currency_convert(price, currency):
    """Convert price to specified currency"""
    if not price:
        return 0
    
    try:
        price = Decimal(str(price))
        
        if currency == 'KES':
            return price * 150  # USD to KES rate
        elif currency == 'NGN':
            return price * 800  # USD to NGN rate
        else:  # USD
            return price
    except:
        return price * 150  # Default to KES

@register.filter
def currency_symbol(currency):
    """Get currency symbol"""
    symbols = {
        'USD': '$',
        'KES': 'KShs.',
        'NGN': '₦'
    }
    return symbols.get(currency, 'KShs.')

@register.filter
def multiply(value, arg):
    """Multiply filter"""
    try:
        return float(value) * float(arg)
    except:
        return 0
