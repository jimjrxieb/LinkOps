FROM postgres:16
ENV POSTGRES_USER=linkops
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_DB=linkops_core
COPY init.sql /docker-entrypoint-initdb.d/ 