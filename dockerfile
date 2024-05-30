# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV SECRET_KEY your_secret_key
ENV DJANGO_DEBUG True  # Set to False in production

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wbe.wsgi:application"]