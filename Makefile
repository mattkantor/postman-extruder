init:
	python3 -m venv venv; \
	echo 'source venv/bin/activate' >> .env; \
	echo 'export DATABASE_URL=""' >> .env; \
	source ./venv/bin/activate; \
	pip3 install -r requirements.txt; \

crawl:
	python instabot/crawl.py

server:
	python manage.py runserver

test:
	py.test ./tests


update_deps:
	source ./venv/bin/activate; \
	pip3 install --upgrade -r requirements.txt; \

fake:
	python -m seed.seed

revision:
	python manage.py db revision --autogenerate;

upgrade:
	python manage.py db upgrade

downgrade:
	python manage.py db downgrade
