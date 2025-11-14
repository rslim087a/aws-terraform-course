FROM python:3.11-slim

WORKDIR /app

RUN pip install flask requests

COPY app/app.py .
COPY app/templates ./templates

EXPOSE 80

CMD ["python", "app.py"]
