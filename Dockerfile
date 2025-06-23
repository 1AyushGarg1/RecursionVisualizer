# Use official Python image
FROM python:3.11-slim

# Install system dependencies, including Graphviz
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of your app
COPY . .

# Expose port (change if your app uses a different one)
EXPOSE 8080

# Start your server
# CMD ["python", "app.py"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
# or for FastAPI: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
