#!/bin/bash

flask db upgrade

exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 restapi.asgi:application 