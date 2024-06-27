#!/bin/bash

########### DB #############
# Initialization
#flask db init

# Generate migrations
flask db migrate

# Apply migrations
flask db upgrade

# Start RQ worker for the 'emails' queue
rq worker emails &

# entry point of developmetn app
exec poetry run uvicorn --reload 'restapi.application:create_application' --host 0.0.0.0 --port 8000 --factory