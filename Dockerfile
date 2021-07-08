FROM python:3.8.10-alpine3.13

WORKDIR /usr/src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api_server ./

ENV PYTHON_ENV=production
EXPOSE 5000
CMD [ "uvicorn", "--factory", "main:create_app" ]
