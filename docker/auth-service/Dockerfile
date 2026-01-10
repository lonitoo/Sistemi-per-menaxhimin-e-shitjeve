FROM python:3.11-slim


WORKDIR /app


COPY sales-system/backend/auth-service/requirements.txt ./requirements.txt


RUN pip install --no-cache-dir -r requirements.txt


COPY sales-system/backend/auth-service /app


EXPOSE 8001


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
