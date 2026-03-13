install:
	pip install -r requirements.txt

run:
	python manage.py runserver

test:
	python manage.py test

migrate:
	python manage.py migrate
