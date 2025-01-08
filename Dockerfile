# Stage 1: Builder
FROM python:3.12.3-slim AS builder

WORKDIR /app

# Install system dependencies required for building
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==2.0.0

# Copy only the poetry files to leverage caching
COPY pyproject.toml poetry.lock LICENSE.md ./

#Configure Poetry and Install Dependencies (no virtualenvs and silence export warnings)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Stage 2: Runner
FROM python:3.12.3-slim AS runner

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m appuser

# Copy installed packages and binaries from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/* /usr/local/bin/

# Copy Poetry config from builder
# NOTE: This is a workaround to ensure the Poetry config is copied correctly, see https://github.com/python-poetry/poetry/issues/6459#issuecomment-2255631116
USER appuser
COPY --from=builder /root/.config/pypoetry /home/appuser/.config/pypoetry

# Copy the application code
COPY . .

# Set ownership to appuser
USER root
RUN chown -R appuser:appuser /app /home/appuser/.config
USER appuser

# Expose the application port
EXPOSE 8130

# Run the application using Poetry
CMD ["poetry", "run", "uvicorn", "src.python_src.api:app", "--host", "0.0.0.0", "--port", "8130"]
