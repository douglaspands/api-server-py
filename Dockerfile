FROM python:3.8.10-alpine3.13

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./topaz_test ./topaz_test

CMD [ "python", "topaz_test" ]
