FROM python:3

LABEL maintainer="Alexandr Topilski <support@fastogt.com>"

COPY . /app
COPY docker/db_config.py /app/app/config/
WORKDIR /app

RUN git submodule update --init --recursive
RUN pip install -r requirements.txt

EXPOSE 8080 6000
CMD [ "python", "server.py" ]
