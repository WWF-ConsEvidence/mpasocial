# MPASocial API

## Stack

- [Django](https://www.djangoproject.com/) (Python)
- [Gunicorn](https://gunicorn.org/) (wsgi)
- [Nginx](https://www.nginx.com/) (webserver)
- [Supervisor](http://supervisord.org/) (process control)
- [Debian](https://www.debian.org/releases/stretch/) (OS)
- [Docker](https://www.docker.com/) (container)

## Local Development Workflow

Common workflow tasks are wrapped up using [Fabric](http://www.fabfile.org/) commands. Refer to `fabfile.py` for the
current commands. Add commands as required.

## Local Development Setup

### Installation

This project uses Docker for configuring the development environment and managing it. By overriding the container's
environment variables, the same Docker image can be used for the production service. Thus, for development work, you
must have Docker installed and running. You will also need a local Python environment; some kind of virtualization is recommended (e.g. [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)), in which you should run `pip install --upgrade -r requirements_dev.txt`.

#### Environment variables

The following are the redacted key-val pairs for a local MPASocial `.env` file or for Elastic Beanstalk configuration
settings:

```
ENV=local
DJANGO_SECRET_KEY=
ADMINS=
ALLOWED_HOSTS=
DB_NAME=mpasocial
DB_HOST=mpasocial_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
PGPASSWORD=postgres
AWS_BACKUP_BUCKET=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
```

#### Local environment initialization

Once Docker is installed and local environment variables set, run the following:

```sh
$ fab buildnocache
$ fab up
```

If this is the first time running the up command, the api image will be built and postgis image will be downloaded. Then
the containers will be started.

With a database already created and persisted in an S3 bucket via

```sh
$ fab dbbackup
``` 
,

```sh
$ fab dbrestore
``` 

will recreate and populate the local database with the latest dump. Without the S3 dump (i.e. running for the first
time), you'll need to create a local database and then run

 ```sh
$ fab migrate
``` 

to create its schema.

A shortcut for the above steps, once S3 is set up, is available via:

```
$ fab freshinstall --keyname [env]

env: local (default), dev, prod
```

### Running the Webserver

Once everything is installed, run the following to have the API server running in the background:

```sh
$ fab runserver
```

### Further

The project directory `api` is mounted to the container, so any changes you make outside the container (e.g. using an
IDE installed on your host OS) are available inside the container.

Please note that running `fab up` does NOT rebuild the image. So if you are making changes to the Dockerfile, for
example adding a dependency to the `requirement.txt` file, you will need to do the following:

```
$ fab down  // Stops and Removes the containers
$ fab build  // Builds a new image
$ fab up
```

> Note: this will delete your local database; all data will be lost.

### Database commands

```
$ fab dbbackup:<env>

env: local, dev, prod
```

Backup the database from a named S3 key

```
$ fab dbrestore:<env>

env: local, dev, prod
```

## Deployments

This project does not yet have CI set up; instead, `/eb_deploy.sh` will create a new version of the application from 
the current local git `HEAD` and update Elastic Beanstalk with it. For this to work you will need the AWS CLI 
installed locally and configured with the appropriate profile and credentials:
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html  
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-profiles

See also the variables and their defaults in `/eb_deploy.sh`; if the AWS setup changes, these will need to likewise 
be changed to reflect the new names and locations or resources.

Once the AWS environment and `/eb_deploy.sh` variables are set, `fab` commands can be quickly run to deploy:

```
fab deploy --envir dev --profile mpasocial
fab deploy --envir master --profile mpasocial
```
