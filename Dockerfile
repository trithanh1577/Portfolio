FROM python:3.12-slim

# Print logs immediately, so they show up in the Render Logs panel in order
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Only the RUNTIME dependencies go into the image. pytest and ruff are
# development tools: they live in requirements-dev.txt and run in CI, not here.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Lab 3, Task A (done): the port comes from the PORT environment variable.
# Render sets PORT; locally it defaults to 8000.
ENV PORT=8000
EXPOSE 8000
# exec: uvicorn (not the shell) receives the stop signal from the platform
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
