# ISI Datamart

This git repository contains the ISI Datamart using REST endpoints.

The content of the Datamart is a set of datasets, which in turn consists of one or more variables. The Dataset Metadata Schema and the Variable Metadata schema are described here: [Metadata Schema](https://datamart-upload.readthedocs.io/en/latest/)

The canonical data format used by the Datamart is the text delimited file (CSV). Details of the canonical data format and examples are here: [Canonical Data Format](https://datamart-upload.readthedocs.io/en/latest/download/)

Using the default configuration the Datamart REST URL is `http://localhost:5000/`. The details of the individual REST endpoints are described here: [Datamart REST API](https://datamart-upload.readthedocs.io/en/latest/api/)

See examples in the Datamart Demo Jupyter notebook for sample usage: [Datamart Data API Demo](Datamart Data API Demo.ipynb)

## Configuration

Create a copy of `config.py` in `instance/config.py`. Change the Postgres user password.

## Running the System

Change directory to `dev-env` and run

    docker-compose up

The docker compose yaml file, `docker-compose.yml`, uses docker compose version 3.7.

On start up Postgres checks if the `postgres` volume exists. If it does not exist, the volume is created using the contents of the `data/postgres/datamart.sql.gz` file.

The ISI Datamart REST endpoints is `http://localhost:5000/`.

## Datasets

The Datamart comes with a few datasets pre-loaded. They include data from OECD, FSI, UAZ and WGI.

## Managing the Datamart Database

### Backing up the existing database

To backup the current Postgres database, run

    docker exec -it datamart-postgres /bin/bash
    # From inside the docker container
    psql --username postgres --password <password> | gzip > /backup/datamart-backup.sql.gz

The backup file is place in the `dev-env/data/postgres` directory.

### Adding datasets directly to the database

To add additional datasets in the form of a TSV file, switch to the scripts directory and run

    python import_tsv_postgres.py <filepath/to/tsv/file>

The script assumes the default Postgres username and password in `config.py`.

### Wiping existing database and updating with new content

To delete the existing database use the `--volumes` option to bring down docker compose. This command destroy the `postgres` volume.

    docker-compose down --volumes

Replace the `dev-env/data/postgres/datamart.sql.gz` file with the new `.sql.gz` file.

And, restart the system.

    docker-compose up
