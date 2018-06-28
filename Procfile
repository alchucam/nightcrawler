web: gunicorn nightcrawler.wsgi --log-file -
worker: celery -A nightcrawler worker --loglevel=info -P eventlet
beat: celery -A nightcrawler beat --loglevel=info
