FROM python:3
COPY . /app
RUN pip install flask urllib3
CMD ["./app/app.py"]

EXPOSE 5000