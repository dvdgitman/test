FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY main.py .

# Run unbuffered to ensure logs show up in CloudWatch immediately
CMD ["python", "-u", "main.py"]
