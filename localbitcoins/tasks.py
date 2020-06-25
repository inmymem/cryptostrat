from celery import Celery
from celery.decorators import task
# from time import sleep
import telegram.bot as telegram
from localbitcoins.notifications import update_notifications

app = Celery()

@app.task(name = 'update_localbitcoins_notifications') 
def get_localbitcoins_notifications():
    update_notifications()

#def tt():
    #telegram.send_debug_message('celery test 3')
# def print_name(duration):
#     telegram.send_debug_message('celery test')
#     return None