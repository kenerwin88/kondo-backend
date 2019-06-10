FROM python:3.7.3-alpine3.9

# Install Packages
RUN apk --no-cache add curl alpine-sdk libffi-dev openssl-dev

# Install Poetry
RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-interaction

COPY . /app

ENTRYPOINT python run_api_server.py