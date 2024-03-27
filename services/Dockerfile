FROM python:3.11-alpine3.18
ENV PYTHONUNBUFFERED=1

RUN mkdir /service
COPY pyproject.toml /service/pyproject.toml
WORKDIR /service

# Install dependencies with poetry
RUN \
  pip install -U pip && \
  pip install poetry && \
  poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi

COPY ./service /service/service

CMD ["python", "-m", "service"]
