import random

def get_stock_trends(technical_change, public_perception):
    # the time period between the turns in weeks
    period = random.randint(5, 10)
    
def get_stock_trends(headline, comments, public_perception, technical_impact):
    # the time period between the turns in weeks
    period = random.randint(5, 10)
    price = 0
    if public_perception > 10:
        price = 1.1 * price
    else:
        price = 0.9 * price
    if technical_impact > 10:
        price = 1.1 * price
    else:
        price = 0.9 * price
    return price