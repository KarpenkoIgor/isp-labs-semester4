from django.db import models

def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_cost'), models.Count('id'))
    if cart_data.get('total_cost__sum'):
        cart.total_cost= cart_data['total_cost__sum']
    else:
        cart.total_cost = 0
    cart.total_products = cart_data['id__count']
    cart.save()
