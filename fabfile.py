"""
Project Command File. Add any helper type commands here for automating
local workflow tasks.

For adding commands and using other Fabric.API comamnds,
    see: http://docs.fabfile.org/en/1.12/tutorial.html

Example of calling the up command:
    $ fab up
"""

import time
from invoke import run, task


# HELPER FUNCTIONS #


def _api_cmd(cmd):
    """Prefix the container command with the docker cmd"""
    return f"docker exec -it mpasocial_api {cmd}"


def local(command):
    run(command, pty=True)


# FABRIC COMMANDS #


@task
def build(c):
    """Run to build a new image prior to fab up"""
    local("docker-compose build")


@task(aliases=["build-nocache"])
def buildnocache(c):
    """Run to build a new image prior fab up"""
    local("docker-compose build --no-cache --pull")


@task
def up(c):
    """Create and start the mermaid-api services
    Note: api_db takes a minute or more to init.
    """
    local("docker-compose up -d")


@task
def down(c):
    """Stop and remove the mermaid-api services"""
    local("docker-compose down")


@task
def runserver(c):
    """Enter Django's runserver on 0.0.0.0:8080"""
    local(_api_cmd("python manage.py runserver 0.0.0.0:8080"))


@task
def collectstatic(c):
    """Run Django's collectstatic"""
    local(_api_cmd("python manage.py collectstatic"))


@task
def makemigrations(c):
    """Run Django's makemigrations"""
    local(_api_cmd("python manage.py makemigrations"))


@task
def migrate(c):
    """Run Django's migrate"""
    local(_api_cmd("python manage.py migrate"))


@task
def shell(c):
    """ssh into the running container"""
    local("docker exec -it mpasocial_api /bin/bash")


@task
def dbshell(c):
    local(_api_cmd("python manage.py dbshell"))


@task
def shellplus(c):
    """Run Django extensions's shell_plus"""
    local(_api_cmd("python manage.py shell_plus"))


@task
def dbrestore(c, keyname="local"):
    """Restore the database from a named s3 key
        ie - fab dbrestore --keyname dev
    """
    local(_api_cmd(f"python manage.py dbrestore {keyname}"))


@task
def dbbackup(c, keyname="local"):
    """Backup the database from a named s3 key
        ie - fab dbbackup --keyname dev
    """
    local(_api_cmd(f"python manage.py dbbackup {keyname}"))


@task
def freshinstall(c, keyname="local"):
    down(c)
    buildnocache(c)
    up(c)

    time.sleep(20)
    dbrestore(c, keyname)
    migrate(c)


@task
# Env options: dev, master
def deploy(c, envir="dev", profile=None):
    """Deploy to Elastic Beanstalk with a specific environment using an AWS profile,
        e.g. fab deploy --profile mpasocial
        requires awscli (`pip install -r requirements_dev.txt` from within local virtual env)
        also requires permissions bit on eb_deploy.sh (`chmod +x eb_deploy.sh`)
    """
    # With a role-based AWS profile we could just set a profile default here
    if profile is None:
        exit("AWS profile must be specified")

    local(f"./eb_deploy.sh -e {envir} -p {profile}")
