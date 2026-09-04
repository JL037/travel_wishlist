# Use an official, lightweight Python image
FROM python:3.11-slim

# Set environment variables for safer builds
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies for psycopg2 and other libraries
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies separately for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app’s code
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run pending Alembic migrations, then start FastAPI in production (no
# --reload). Baked into CMD rather than relying on a platform's separate
# "pre-deploy command" feature - simpler to reason about and always in sync
# with whatever image actually gets started.
CMD ["sh", "-c", "python -m alembic stamp 47c18d3434d2 && python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
