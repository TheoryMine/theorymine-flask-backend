from invoke import task
import os

@task
def prepare_test_env(c):
    os.environ['DATABASE_HOST']='localhost'
    os.environ['DATABASE_USER']='root'
    os.environ['DATABASE_PASSWORD']=''
    os.environ['DATABASE_NAME']='theorymine-test'


@task
def migrate_up(c):
    c.run("db-migrate simple-db-migrate.conf")

@task(help={'name': "Name of the migration. should contain only lower case char or _"})
def create_migration(c, name):
    c.run("db-migrate -n {}".format(name))

@task()
def start_dev(c):
    c.run("export FLASK_APP=app")
    c.run("FLASK_ENV=development flask run")

@task(prepare_test_env, migrate_up)
def test(c):
    c.run("python -m pytest tests -s")\

@task
def deploy(c):
    c.run("pip freeze > requirements.txt")
