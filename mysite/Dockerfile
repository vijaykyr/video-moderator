# Set the base image to Ubuntu
FROM ubuntu

# Expose port
EXPOSE 80

# Update the sources list
RUN apt-get update

# Install python, pip
RUN apt-get install -y python2.7 python-pip

# Install Google API python client
RUN pip install --upgrade google-api-python-client

# Install Django, web framework
RUN pip install django==1.9

# Install Open Computer Vision python module, used for extracting stills from video
RUN apt-get install -y python-opencv

# Copy application to container (assumes code is in current directory)
ADD . /mysite 

# Set the default directory where CMD will execute
WORKDIR /mysite

# This gets rid of the "libdc1394 error: Failed to initialize libdc1394" warning
# Edit: Figure out why this command doesn’t take unless you run it from inside the container
RUN ln /dev/null /dev/raw1394

#If running locally set application default credentials. If running in production you don't need this
ENV GOOGLE_APPLICATION_CREDENTIALS='/mysite/keys/975c65f89649.json'

# Start webserver
CMD python manage.py runserver 0.0.0.0:80
