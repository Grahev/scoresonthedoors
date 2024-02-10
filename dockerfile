# Use an official Python 3.11 runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /usr/src/app/

#django crone logfile

# Create a cron directory
RUN mkdir /cron

#install cron
RUN apt-get update && apt-get -y install cron

# Add cron job file
#COPY cronjob /etc/cron.d/cronjob

# Give execution rights on the cron job
#RUN chmod 0644 /etc/cron.d/cronjob

# Create the log file
# RUN touch /cron/django_cron.log
# RUN chmod 777 /cron/django_cron.log



# RUN service cron start

# RUN python manage.py crontab add

# RUN service cron restart



# # Run the cron command
# CMD ["cron", "-f"] #test