FROM python:3.12-slim

WORKDIR /app

# Update system packages and fix zlib1g vulnerability
RUN apt-get update && apt-get install --only-upgrade -y zlib1g && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"] 