# Alpine OS with preinstalled python distribution
FROM python:3.9-alpine

# working directory
WORKDIR /app

# Copy everything from the docker directory to working directory
COPY /requirements.txt /app

RUN pip3 install -r requirements.txt
RUN pip3 install uvicorn

COPY wiki_service /app/wiki_service

CMD [ "python", "-m", "wiki_service.main" ]