FROM python:3.9-slim

# TODO: You need to copy the project files to the Docker and install the dependencies
COPY . /app
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["/bin/bash", "bin/run"]
