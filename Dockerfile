# Use an official Python slim image.
FROM python:3.11-slim

# Set the working directory.
WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*


# Copy and install dependencies.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application.
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables for FastAPI and database.
ENV PYTHONUNBUFFERED=1

# Expose port 80 for the FastAPI app.
EXPOSE 80

# Run the FastAPI application using uvicorn.
ENTRYPOINT ["/entrypoint.sh"]