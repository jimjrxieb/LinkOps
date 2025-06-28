FROM python:3.12-slim

WORKDIR /app

# Update all system packages to fix vulnerabilities including zlib1g
RUN apt-get update && apt-get upgrade -y && apt-get install -y --only-upgrade zlib1g && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"] 