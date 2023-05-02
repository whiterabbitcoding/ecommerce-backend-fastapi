from sql_app import models


def get_total_for_cart(cart: models.Cart) -> int:
    cartitems = cart.cartitems
    total = 0
    for item in cartitems:
        item_total = item.quantity * item.item.price
        total += item_total
    return total
