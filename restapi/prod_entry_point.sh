#!/bin/bash


# To set the revision in the database to the head, without performing any migrations.
# You can change head to the required change you want.
flask db stamp head
# To detect automatically all the changes.
flask db migrate
# To apply all the changes
flask db upgrade

exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 'restapi.application:create_application()' 

#exec poetry run uvicorn --reload restapi.asgi:application --host 0.0.0.0 --port 8000