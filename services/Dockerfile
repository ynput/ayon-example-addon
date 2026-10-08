FROM python:3.11-alpine3.18
ENV PYTHONUNBUFFERED=1

RUN mkdir /service
COPY pyproject.toml /service/pyproject.toml
WORKDIR /service

RUN pip install --break-system-packages -e .

COPY ./service /service/service

CMD ["python", "-m", "service"]
