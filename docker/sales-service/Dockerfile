
FROM python:3.11-slim


WORKDIR /app


COPY sales-system/backend/sales-service/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY sales-system/backend/sales-service .


EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
