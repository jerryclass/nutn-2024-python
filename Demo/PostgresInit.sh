./nt_db_postgres.sh stop
docker rm nutn-my-postgres-container
docker rmi nutn-my-postgres
./nt_db_postgres.sh start
