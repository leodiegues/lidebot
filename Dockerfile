FROM python:3.9.9-slim

ENV POETRY_VERSION 1.1.11

WORKDIR /app

RUN pip install 'poetry==${POETRY_VERSION}'

RUN python -m poetry install --no-dev

COPY scripts/ scripts

RUN chmod +x ./scripts/run_crawlers.sh
RUN chmod +x ./scripts/publish_thread.sh

