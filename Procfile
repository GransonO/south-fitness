release: bash ./release-tasks.sh
web: gunicorn rfh_server.wsgi —-log-file -
worker: python manage.py qcluster