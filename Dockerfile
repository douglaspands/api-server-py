ARG PYTHON_VERSION=3.8.11-alpine3.14


FROM python:${PYTHON_VERSION} as base

RUN apk add postgresql-libs


FROM base as builder

RUN apk add alpine-sdk python3-dev gcc postgresql-dev musl-dev libc-dev linux-headers libffi-dev rust cargo make 
COPY requirements.txt ./
RUN pip install --no-cache-dir --prefix="/install" -r /requirements.txt


FROM base as release

COPY --from=builder /install /usr/local

ENV PYTHONUNBUFFERED=1 \
    PYTHON_ENV=production \
    PYTHONPATH=/app \
    PORT=8000

WORKDIR /app/
EXPOSE 8000

COPY ["scripts/start.sh", "scripts/prestart.sh", "scripts/gunicorn_conf.py", "alembic.ini", "./"]

COPY ./apiserver ./apiserver
COPY ./migrations ./migrations

CMD ["sh", "./start.sh"]
