import os

bind = "127.0.0.1:8000"
backlog = 2048
workers = 4
keepalive = 2
accesslog = os.path.dirname(__file__) + '/access.log'
errorlog = os.path.dirname(__file__) + '/error.log'
