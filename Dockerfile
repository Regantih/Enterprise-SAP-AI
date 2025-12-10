# Athena Core - Enterprise AI Agent System
FROM python:3.12-slim

LABEL maintainer="Athena Core Team"
LABEL description="Multi-agent AI system for SAP enterprise workflows"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY athena_system/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY athena_system/ ./athena_system/

# Create non-root user for security
RUN useradd -m -u 1000 athena && chown -R athena:athena /app
USER athena

# Expose port
EXPOSE 8000

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the server
CMD ["python", "-m", "athena_system.web_ui.server"]
