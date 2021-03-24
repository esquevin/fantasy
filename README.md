## Fantasy sport simulator

You should setup yourself a virtualenv

A common way to manage virtualenv nowadays is through pyenv:

`brew install pyenv pyenv-virtualenv`

`pyenv virtualenv 3.7.7 fantasy`

Install the dependencies

`make install`

## Play with it

You can run the tests.

`make test`

Or you can run a server and uses its admin panel. You'll need to create a super user first:

`python manage.py createsuperuser`

Start the webserver

`make run`

Access the administration with your newly created super user

`open http://localhost:8000/admin`