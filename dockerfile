# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Set environment variables
ENV SECRET_KEY=${SECRET_KEY}
ENV DJANGO_DEBUG=${DJANGO_DEBUG}
ENV STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY}
ENV STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
ENV SENTRY_DSN=${SENTRY_DSN}
ENV SUPERUSER_USERNAME=${SUPERUSER_USERNAME}
ENV SUPERUSER_EMAIL=${SUPERUSER_EMAIL}
ENV SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD}

# Collect static files
RUN python manage.py collectstatic --noinput

# Create superuser
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('${SUPERUSER_USERNAME}', '${SUPERUSER_EMAIL}', '${SUPERUSER_PASSWORD}')" | python manage.py shell

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wbe.wsgi:application"]
