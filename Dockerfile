ARG PYTHON_VERSION=3.9.5-alpine3.14

FROM python:${PYTHON_VERSION} as base

RUN apk add postgresql-libs


FROM base as builder

RUN apk add alpine-sdk python3-dev gcc postgresql-dev musl-dev libc-dev linux-headers libffi-dev rust cargo

COPY requirements.txt ./
RUN pip install --prefix="/install" -r /requirements.txt


FROM base as release

ENV PYTHONUNBUFFERED=1 \
    PYTHON_ENV=production

COPY --from=builder /install /usr/local

WORKDIR /usr/src
COPY ./api_server ./
    
EXPOSE 8000
CMD [ "uvicorn", "--factory", "main:create_app" ]
