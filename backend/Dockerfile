FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies including tesseract-ocr and build-essential
RUN apt-get update && \
    apt-get install -y tesseract-ocr build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy code into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run FastAPI with live reload (for dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 