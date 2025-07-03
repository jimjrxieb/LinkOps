FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install fastapi uvicorn pydantic

# Optional: For real pipeline execution
# RUN pip install kfp

EXPOSE 8005

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"] 