FROM mysql:8.0

COPY database.sql /docker-entrypoint-initdb.d/01.sql
COPY grants.sql /docker-entrypoint-initdb.d/02.sql
