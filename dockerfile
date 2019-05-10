FROM python:rc-alpine
COPY . /app
RUN make /app
CMD python /app/app.py