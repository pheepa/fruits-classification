FROM python:3.8.1-slim 
# Image from dockerhub

ENV PYTHONUNBUFFERED 1 
EXPOSE 8000 
# Expose the port 8000 in which our application runs
WORKDIR /app 
# Make /app as a working directory in the container
# Copy requirements from host, to docker container in /app 
COPY ./requirements.txt /app/requirements.txt
# Copy everything from ./src directory to /app in the container
COPY ./src /app/src
COPY ./models /app/models
RUN pip install -r /app/requirements.txt
RUN pip install torch==1.13.0+cpu torchvision==0.14.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
# Install the dependencies
# Run the application in the port 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "src.main:app"]