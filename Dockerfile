# default OS image
FROM alpine

RUN apk add --no-cache python3-dev py3-pip && pip3 install --upgrade pip

# working directory
WORKDIR /app

# # Copy everything from the docker directory to working directory
COPY /requirements.txt /app

RUN pip3 install -r requirements.txt

COPY ["MongoDBAPI.py", "/app"]

# Exposing an internal port
EXPOSE 5001

# default commands
ENTRYPOINT [ "python3" ]
CMD ["MongoDBAPI.py"]

