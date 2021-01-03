FROM python:3.9.1
ENV DB_SERVER=
ENV DB_NAME=
ENV DB_USER=
ENV DB_PWD=
ENV LOG_LEVEL=INFO
#Install dependencies
RUN mkdir /opt/transfer
COPY requirements.txt /opt/transfer
RUN pip3 install -r /opt/transfer/requirements.txt

#Copy the binaries
COPY bin /opt/transfer
WORKDIR /opt/transfer

EXPOSE 8081
#Wait for DB sever to start and then start the web server
ENTRYPOINT python3 dbtest.py && \
          gunicorn --bind "0.0.0.0:8081" --log-level=$LOG_LEVEL --access-logfile - 'transfer:app'