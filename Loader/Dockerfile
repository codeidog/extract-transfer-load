FROM python:3.9.1
ENV SERVER_URL=
ENV LOG_LEVEL=
#Install dependencies
RUN mkdir /opt/loader
COPY requirements.txt /opt/loader
RUN pip3 install -r /opt/loader/requirements.txt

#Copy the binaries
COPY bin /opt/loader
WORKDIR /opt/loader

#--access-logfile -
ENTRYPOINT python3 main.py --url $SERVER_URL --log $LOG_LEVEL