from celery import Celery
from celery.decorators import task
from .update_prices import update_gbpbtc_price

app = Celery()

@app.task(name="reference_price_update_gbpbtc_price")
def update_all_prices():
    update_gbpbtc_price()
