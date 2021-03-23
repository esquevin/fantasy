open_model: models.png
	open models.png

models.png: */models.py
	python manage.py graph_models -g -o models.png

clean:
	rm -f models.png
	rm -f db.sqlite3
	