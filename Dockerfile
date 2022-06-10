# Alpine OS with preinstalled python distribution
FROM python:3.9-alpine

# working directory
WORKDIR /app

# Copy everything from the docker directory to working directory
COPY /requirements.txt /app

RUN pip3 install -r requirements.txt
RUN pip install fastapi uvicorn

COPY ["wiki_service", "/app"]

# Exposing an internal port
EXPOSE 5001

CMD [ "uvicorn", "wiki_service.main:wiki", "--host", "0.0.0.0", "--port", "5001"]