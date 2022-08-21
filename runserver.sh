python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

gunicorn --worker-tmp-dir /dev/shm kuntcrm.wsgiru