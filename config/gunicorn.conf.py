import multiprocessing



def when_ready(server):
    open('/tmp/app-initialized', 'w').close()
    
bind = 'unix:///tmp/nginx.socket'
#workers = multiprocessing.cpu_count() * 2 + 1
workers = multiprocessing.cpu_count() + 1
timeout = 10  # could be lower
preload_app = True
# import multiprocessing

# bind = "127.0.0.1:8000"
# workers = multiprocessing.cpu_count() * 2 + 1



# def when_ready(server):
#     open('/tmp/app-initialized', 'w').close()


# bind = 'unix:///tmp/nginx.socket'
# worker_class = 'gevent'  # not necessary
# timeout = 90  # not necesssary

#worker_class = 'gevent'  # not necessary
