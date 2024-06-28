#!/bin/bash

# Start RQ worker for the 'emails' queue
rq worker emails &

# entry of the production app
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 'restapi.application:create_application()' 