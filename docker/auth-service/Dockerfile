# =========================
# AUTH SERVICE DOCKERFILE
# =========================

FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY sales-system/backend/auth-service/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy auth service code
COPY sales-system/backend/auth-service /app

# Expose port
EXPOSE 8001

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
