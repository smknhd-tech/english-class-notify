FROM python:3.8-slim

COPY pyproject.toml poetry.lock ./ \
    notify.py ./

RUN pip install poetry \
    && poetry config virtualenvs.create false\
    && poetry install \
    && touch config.txt

