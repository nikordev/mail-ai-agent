FROM python:3.12-slim

WORKDIR /app

COPY . .

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install poetry
RUN poetry install --without dev

EXPOSE 8000

CMD ["poetry", "run", "agent"]