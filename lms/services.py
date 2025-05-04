import os

import stripe

from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(name):
    """Создание продукта в Stripe"""

    # Создание продукта
    product = stripe.Product.create(
        name=name,
    )

    return product


def create_stripe_price(amount, product):
    """Создание цены в Stripe"""

    # Создание цены
    price = stripe.Price.create(
        product=product.id,
        unit_amount=amount * 100,
        currency="rub",
    )

    return price


def create_stripe_session(price):
    """Создание сессии в Stripe"""

    stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )

    # Создание сессии
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    return session.id, session.url
