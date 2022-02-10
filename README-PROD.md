# TAX INNOVATION

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

- [Python 3.8.\*](https://www.python.org/downloads/)
- [Pipenv](https://pipenv-es.readthedocs.io/es/latest/): To install the python dependencies
  - You can install with `python -m pip install pipenv`
- [Graphviz](https://graphviz.gitlab.io/). Only if you want to generate the DB graph models.
  - **Note:** Add graphivz binaries folder to PATH Variables.
- [PostgreSQL 11+](https://www.postgresql.org/download/)
- [weasyprint](https://weasyprint.readthedocs.io/en/latest/install.html)
- [GTK+ 64 Bit](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer) For Windows environments
- Make sure you have a tmp folder at the raice of your system

### Installing

#### Installing WeasyPrint

If you use anacoda environments on Windows OS create the next file:

```python
"""
    sitecustomize.py
    ================

    To ensure the correct GTK3 Runtime

    - To activate the GTK for Anaconda and all its environments:
      put the file into **sys.base_prefix**,
      i.e. the path where Anaconda's master python.exe is located.
      i.e. your Anaconda install directory

    - To activate the GTK only in a dedicated environment:
      put the file into the **./Lib/site-packages** folder of that
      environemt
"""
import os

# insert the GTK3 Runtime folder at the beginning
GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
```

More Info: [weasyprint](https://weasyprint.readthedocs.io/en/latest/install.html)

#### Instaling DB

Create the database and connect to it

```bash
psql -U postgres
```

Create the user and custom settings

```psql
postgres=# CREATE USER {YOUR_POSTGRES_USER} WITH PASSWORD '{YOUR_PASSWORD}';
postgres=# ALTER ROLE {YOUR_POSTGRES_USER} WITH LOGIN;
postgres=# ALTER ROLE {YOUR_POSTGRES_USER} SET client_encoding TO 'utf8';
postgres=# ALTER ROLE {YOUR_POSTGRES_USER} SET default_transaction_isolation TO 'read committed';
postgres=# ALTER ROLE {YOUR_POSTGRES_USER} SET timezone TO 'America/Mexico_City';
```

Create tables and schemas

```psql
postgres=# CREATE DATABASE taxinnovation;
postgres=# ALTER DATABASE taxinnovation OWNER TO {YOUR_POSTGRES_USER};
postgres=# \c taxinnovation;
taxinnovation=# CREATE SCHEMA taxinnovation;
taxinnovation=# GRANT ALL PRIVILEGES ON SCHEMA taxinnovation TO {YOUR_POSTGRES_USER};
taxinnovation=# DROP SCHEMA public;
```

Grant permissions

```psql
taxinnovation=# GRANT ALL PRIVILEGES ON DATABASE taxinnovation TO {YOUR_POSTGRES_USER};
```


## Development

### Generate Graph Models

Create a PNG graph models

```shell
pipenv run python manage.py graph_models -a -g -o rh.png
```

Or create a PDF graph models

```shell
pipenv run python manage.py graph_models -a -g -o rh.pdf
```

[More Info](https://django-extensions.readthedocs.io/en/latest/graph_models.html)


### Loaddata

```shell script
./manage.py loaddata taxinnovation/fixtures/catalogs.postalcode.json.bz2
```

Add the next register in [django sites](http://localhost:8000/admin/sites/site/1/change/):

http://localhost:8000

## Running the tests

```shell script
$ pipenv run pytest --ds=config.settings.test -s
```

## Docker deploy

Autenticación de gcloud con docker

```bash
gcloud auth configure-docker
```

Asegurarse de que está seleccionado el proyecto donde se implementará el sistema.

```bash
gcloud config set project tax-innovation-produccion
```

Obtener credenciales del proyecto y seleccionar el cluster correspondiente

```bash
gcloud container clusters get-credentials taxt-innovation-prod --zone us-central1
```

Creación de nombre de espacio (Sólo la primera vez)

```bash
kubectl create namespace tax-innovation-prod
```

Configurar por default el namespace

```
kubectl config set-context --current --namespace=tax-innovation-prod
```

Cargar los secrets

```bash
kubectl create secret generic variables-taxt-innovation-back-prod --from-env-file=./.secrets.local-prod.txt --namespace=tax-innovation-prod
```

Generar imagen de docker y publicarla.

```bash
docker build -f compose/production/django/Dockerfile . -t gcr.io/tax-innovation-produccion/tax_innovation_backend_prod:x.x.x.x
docker push gcr.io/tax-innovation-produccion/tax_innovation_backend_prod:x.x.x.x
```

Desplegar el Balanceador de cargas

 ```bash
 kubectl apply -f service.yaml
 ```

Desplegar el contenedor en los pods (Cambiar el tag de la imagen en el archivo deployment.yaml)

```bash
kubectl apply -f deployment.yaml
```
## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

- **Ramses Martinez** - _Initial work_ - [RamsesMartinez](https://github.com/RamsesMartinez)
- **Mauricio Olascoaga**

## License

Thi work is under exclusive copyright.
