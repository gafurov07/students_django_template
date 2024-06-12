mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
csu:
	python3 manage.py createsuperuser
cr:
	python3 manage.py migrate django_celery_results
cel:
	celery -A root worker -l INFO