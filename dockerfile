FROM python:rc-alpine
COPY . /app
CMD python /app/app.py