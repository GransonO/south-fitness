release: bash ./release-tasks.sh
web: gunicorn south_fitness_server.wsgi —-log-file -
worker: python manage.py qcluster