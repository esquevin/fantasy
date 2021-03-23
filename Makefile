run: migrate
	python manage.py runserver

test: 
	python manage.py test

migrate:
	python manage.py migrate

install:
	pip install -r requirements.txt

open_model: models.png
	open models.png

models.png: */models.py
	python manage.py graph_models -g -o models.png card tournament

clean:
	rm -f models.png
	rm -f db.sqlite3
	