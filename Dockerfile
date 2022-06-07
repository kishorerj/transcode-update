FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


RUN pip install --upgrade -r requirements.txt

# Run the web service on container startup with one worker process and 8 threads.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --chdir app app:app
