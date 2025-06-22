FROM python:3.9-slim

WORKDIR /app

COPY ./src /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9002"] 