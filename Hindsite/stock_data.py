import random
    
def get_stock_trends(company_price, public_perception, technical_impact):
    # the time period between the turns in weeks
    period = random.randint(5, 10)
    points = dict()
    pub_price = 0
    tech_price = 0
    tmp_price = company_price
    for i in range(period):
        if public_perception > 10:
            pub_price = random.uniform(1.1, 1.3) * tmp_price
        else:
            pub_price = random.uniform(0.75, 0.9) * tmp_price
        if technical_impact > 10:
            tech_price = random.uniform(1.1, 1.3) * company_price
        else:
            tech_price = random.uniform(0.75, 0.9) * company_price
        points[i] = pub_price
        tmp_price = pub_price
    points[len(points)-1] = (tech_price + pub_price)/2
    company_price = points[len(points)-1]
    
    return points, company_price
      
    