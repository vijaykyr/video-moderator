# Set the base image to Ubuntu
FROM ubuntu

# Expose port
EXPOSE 8000

# Update the sources list
RUN apt-get update

# Install python, pip and git
RUN apt-get install -y python=2.7.5-5ubuntu3 python-pip=1.5.4-1ubuntu3

# Install Google API python client
RUN pip install --upgrade google-api-python-client

# Install Django
RUN pip install django==1.9

# Copy application to container (assumes code is in current directory)
ADD mysite /mysite 

# Set the default directory where CMD will execute
WORKDIR /mysite

# Start webserver
CMD python manage.py runserver 0.0.0.0:8000