FROM python:3.11.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5678 available to the world outside this container
EXPOSE 9100

# Run server.py when the container launches
CMD ["python", "fastapiserver_9100.py"]