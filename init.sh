#!/bin/bash

# Exit script on any error
set -e

echo "Starting the deployment process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Run Docker Compose to start PostgreSQL and FastAPI
echo "Starting Docker services..."
docker-compose up -d --build

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL to start..."
while ! nc -z localhost 5432; do
  sleep 1
done

# Set database connection details
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mydatabase"
DB_USER="postgres"
DB_PASSWORD="password"

# Run SQL scripts to set up the database
echo "Running SQL scripts to set up the database..."



PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -f ./create-tables.sql

python3 ./populate-tables.py

echo "Database setup completed!"

echo "Application setup complete! You can now access the app."
