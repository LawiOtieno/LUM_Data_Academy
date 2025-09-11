
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
        return price

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

@register.simple_tag
def convert_price(price, currency):
    """Template tag to convert price to currency"""
    if not price:
        return 0
    
    try:
        price = Decimal(str(price))
        
        if currency == 'KES':
            return price * 150
        elif currency == 'NGN':
            return price * 800
        else:  # USD
            return price
    except:
        return price

@register.simple_tag
def get_currency_symbol(currency):
    """Template tag to get currency symbol"""
    symbols = {
        'USD': '$',
        'KES': 'KShs.',
        'NGN': '₦'
    }
    return symbols.get(currency, 'KShs.')
