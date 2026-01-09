# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY sales-system/ui/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app code
COPY sales-system/ui .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "streamlit_test.py", "--server.port=8501", "--server.address=0.0.0.0"]
