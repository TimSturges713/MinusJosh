import random
    
def get_stock_trends(company_price, public_perception, technical_impact):
    # the time period between the turns in weeks
    period = random.randint(5, 10)
    points = dict()
    pub_price = 0
    tech_price = 0
    p_price = company_price
    t_price = company_price

    for i in range(period):
        if public_perception > 10:
            pub_price = random.uniform(1.1, 1.3) * p_price
        else:
            pub_price = random.uniform(0.75, 0.9) * p_price
        if technical_impact > 10:
            tech_price = random.uniform(1.1, 1.3) * t_price
        else:
            tech_price = random.uniform(0.75, 0.9) * t_price
        points[i] = pub_price
        p_price = pub_price
        t_price = tech_price
    points[len(points)-1] = (tech_price + pub_price)/2
    company_price = points[len(points)-1]
    
    return points, company_price

