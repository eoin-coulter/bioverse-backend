# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /code

# Install Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the FastAPI app
COPY ./app /code/app

# Expose the app port
EXPOSE 8000


# Run FastAPI app
CMD ["uvicorn","python", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
