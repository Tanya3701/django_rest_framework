import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(product):
    """Создание продукта в Stripe"""
    product_stripe = stripe.Product.create(name=product.title)
    return product_stripe


def create_price(product_stripe, price):
    """Создание цены на продукт в Stripe"""
    price_stripe = stripe.Price.create(
        currency="rub",
        unit_amount=int(price) * 100,
        product_data={"name": product_stripe},
    )
    return price_stripe


def create_session_id(price_stripe):
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_stripe, "quantity": 1}],
        mode="payment",
    )
    return session["id"], session["url"]
