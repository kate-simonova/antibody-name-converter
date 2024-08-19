# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set the timezone
ENV TZ=Europe/Prague
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python and other necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY App/requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt && \
    pip3 install statsmodels

# Copy the application code into the container
COPY App/ .

# Specify the command to run on container startup
CMD ["python3", "main.py"]
