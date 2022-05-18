# Alpine OS with preinstalled python distribution
FROM python:3.9-alpine

# working directory
WORKDIR /app

# Copy everything from the docker directory to working directory
COPY /requirements.txt /app

RUN pip3 install -r requirements.txt

COPY ["MongoDBAPI.py", "/app"]

# Exposing an internal port
EXPOSE 5001

# default commands
ENTRYPOINT [ "python3" ]
CMD ["MongoDBAPI.py"]
