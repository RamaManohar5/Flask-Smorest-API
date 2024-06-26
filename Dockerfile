ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-alpine as python-base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/usr/local" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/app" \
    PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies required for Poetry installation and building Python packages
RUN apk update \
    && apk add --no-cache python3-dev gcc libc-dev musl-dev libffi-dev curl \
    && pip install poetry --no-cache \
    && apk del curl gcc libc-dev musl-dev \
    && rm -rf /var/cache/apk/*

WORKDIR $PYSETUP_PATH

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --without dev

####################################### Development ##############################################

FROM python:${PYTHON_VERSION}-alpine as development

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYSETUP_PATH="/app" \
    PATH="/usr/local/bin:$PATH"

# Set environment variables for Flask
ENV FLASK_ENV=development \
    FLASK_DEBUG=1

# Copy only the necessary artifacts from the base image
COPY --from=python-base /usr/local /usr/local
COPY --from=python-base /app /app
# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

WORKDIR $PYSETUP_PATH

# Copy application code
#COPY ./restapi ./restapi

# Expose the application port
EXPOSE 8000

# Start command
CMD ["poetry", "run", "uvicorn", "--reload", "restapi.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

####################################### Production ##############################################

FROM python:${PYTHON_VERSION}-alpine as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYSETUP_PATH="/app" \
    PATH="/usr/local/bin:$PATH"

# Set environment variables for Flask
ENV FLASK_ENV=production \
    FLASK_DEBUG=0

# Copy only the necessary artifacts from the base image
COPY --from=python-base /usr/local /usr/local
COPY --from=python-base /app /app

# Copy Poetry configuration files
# COPY pyproject.toml poetry.lock ./

WORKDIR $PYSETUP_PATH

# Copy application code
#COPY ./restapi ./restapi 

# Expose the application port
EXPOSE 80

# Entry point for production
#ENTRYPOINT ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "restapi.asgi:application"]
#ENTRYPOINT [ "gunicorn", "-w", "4", "--bind","0.0.0.0:8500", "restapi:create_app()" ]
CMD ["sh", "./restapi/prod_entry_point.sh"]