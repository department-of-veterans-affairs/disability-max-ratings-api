# Stage 1: Builder
FROM python:3.12.3-slim AS builder

WORKDIR /app

# Install system dependencies required for building
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy only the poetry files to leverage caching
COPY pyproject.toml poetry.lock ./

# Configure Poetry (no virtualenvs and silence export warnings)
RUN poetry config virtualenvs.create false && \
    poetry config warnings.export false && \
    poetry install --only main --no-interaction --no-ansi

# Stage 2: Runner
FROM python:3.12.3-slim AS runner

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m appuser

# Copy installed site-packages and Poetry from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

# Copy the application code
COPY . .

# Set ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8130

# Run the application using Poetry
CMD ["poetry", "run", "uvicorn", "src.python_src.api:app", "--host", "0.0.0.0", "--port", "8130"]
