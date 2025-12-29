FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Run with Gunicorn for production-grade WSGI serving
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "main:app"]
