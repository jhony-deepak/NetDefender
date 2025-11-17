FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install flask requests

EXPOSE 5000

CMD ["python", "dashboard/app.py"]