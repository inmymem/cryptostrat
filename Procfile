web: bin/start-nginx gunicorn -c config/gunicorn.conf.py cryptostrat_project.wsgi:application
beat: celery -A cryptostrat_project beat -l info
worker0: celery -A cryptostrat_project worker -l info
worker1: celery -A cryptostrat_project worker -l info
worker2: celery -A cryptostrat_project worker -l info
worker3: celery -A cryptostrat_project worker -l info
worker4: celery -A cryptostrat_project worker -l info
worker5: celery -A cryptostrat_project worker -l info
#worker: celery -A cryptostrat_project worker -B -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
