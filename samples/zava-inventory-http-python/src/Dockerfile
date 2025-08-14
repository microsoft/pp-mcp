FROM python:3.12.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /code

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /code/

# Expose port 8080 for the SSE server
EXPOSE 8080

# Start the app with uvicorn
CMD ["python", "/code/server.py"]

# Create a non-root user
RUN useradd -m appuser
USER appuser