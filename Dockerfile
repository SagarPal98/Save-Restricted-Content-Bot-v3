FROM python:3.10.13-slim-bookworm

# Install system dependencies
RUN apt update && apt upgrade -y && \
    apt install -y --no-install-recommends \
    git curl wget ffmpeg bash neofetch python3-pip software-properties-common && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start the app directly (only one entry point)
CMD ["python3", "main.py"]
