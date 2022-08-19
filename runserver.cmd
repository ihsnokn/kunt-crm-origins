python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

@REM gunicorn --worker-tmp-dir /dev/shm kuntcrm.wsgiru