FROM postgres:13
ENV DB_NAME=
ENV DB_USER=
ENV DB_PWD=
COPY initdb.sh /docker-entrypoint-initdb.d
RUN  chmod +x /docker-entrypoint-initdb.d//initdb.sh 