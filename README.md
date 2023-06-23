# Conference Management System Backend Testing Environment

This repository contains the testing environment for the backend of a conference management system. It includes the necessary files and instructions to set up the environment.

## Prerequisites

Before setting up the testing environment, make sure you have the following software installed:

- Python 3.11 or higher
- Docker
- Any database management software (preferably DBeaver)

## Docker Setup

To set up the testing environment using Docker, follow these additional steps:

1. Build the Docker image:

```bash
docker build -t <image_name> .
```

2. Run the Docker container:

```bash
docker run -d -p 3306:3306 -p 33060:33060 <image_name>
```

## DBeaver Setup

To setup DBeaver to connect to your MySQL Docker container, follow these steps:

1. Make sure that your Docker container is running in the background.

2. Open DBeaver and select `New Database Connection`.

![new_connection](https://github.com/gokudaisensei/conference-backend-test/assets/87324237/6d0d7a0c-0100-426b-a335-377d2c40bbcf)

3. In the resulting dialog box, select MySQL and click `Next`.

4. The password is available in the `Dockerfile`. Please make sure to either use that or provide your own password before building using the `Dockerfile`. The name of the database is also available in the `init.sql` file. If you would like to use another database name, please make sure to change that as well in the `init.sql` file before building using the `Dockerfile`. Fill the password and database fileds as per your changes and click `Finish`.

## Setup Instructions

Follow these steps to set up the testing environment:

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install project dependencies using Poetry:

```bash
poetry install
```

3. Start the database management software and create a new database connection.

4. Copy the `example.env` file and rename it to `.env`:

```bash
cp example.env .env
```

5. Update the `.env` file with your database connection details.

The connection string has the format:
``` mysql+pymysql://root:<mysql_pwd>@localhost/<db_name>
```

6. Run the Alembic migration to set up the database schema:

```bash
poetry run alembic upgrade head
```

This command will apply any pending database migrations and update the schema to the latest version.

## Testing

To run the tests for the conference management system backend, use the following command:

```bash
poetry run pytest
```

This will execute the test suite and display the test results.
