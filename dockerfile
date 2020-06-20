FROM python:3.8-slim

WORKDIR /tmp/app

COPY pyproject.toml ./ \
    poetry.lock ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY notify/ ./notify/

ENTRYPOINT ["poetry", "run", "python", "-m", "notify.notify"]
CMD ["today"]
