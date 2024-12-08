FROM postgres:latest
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=toor
ENV POSTGRES_DB=db

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/
COPY insert_test_data.sql /docker-entrypoint-initdb.d/

# ENTRYPOINT ["postgres"]
# CMD [ "./docker-entrypoint-initdb.d/init.sql" ]