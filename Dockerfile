# Use the official MySQL Docker image
FROM mysql:latest

# Set the root password (change it to your desired password)
ENV MYSQL_ROOT_PASSWORD=root

# Copy the SQL file to the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the ports
EXPOSE 3306 33060

# Start the MySQL service and bind to all interfaces
CMD ["mysqld", "--bind-address=0.0.0.0"]
