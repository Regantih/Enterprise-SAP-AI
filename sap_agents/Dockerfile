# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (Netflix-grade: Slim, Secure, Fast)
FROM python:3.10-slim

WORKDIR /app

# Create non-root user for security
RUN groupadd -r antuser && useradd -r -g antuser antuser

# Copy dependencies from builder
COPY --from=builder /root/.local /home/antuser/.local
COPY . .

# Set environment variables
ENV PATH=/home/antuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=web_ui/server.py

# Switch to non-root user
USER antuser

# Expose port
EXPOSE 8000

# Healthcheck (Resilience)
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1

# Run the application
CMD ["python", "web_ui/server.py"]
