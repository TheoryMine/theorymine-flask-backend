from invoke import task
import os

@task
def prepare_test_env(c):
    os.environ['DATABASE_HOST']=os.getenv("DATABASE_HOST") or 'localhost'
    os.environ['DATABASE_USER']=os.getenv("DATABASE_USER") or 'root'
    os.environ['DATABASE_PASSWORD']=os.getenv("DATABASE_PASSWORD") or ''
    os.environ['DATABASE_NAME']=os.getenv("DATABASE_NAME") or'theorymine-test'
    os.environ['STRIPE_SECRET_KEY']='fake-stripe-key'
    os.environ['STRIPE_PUBLISHABLE_KEY']='fake-stripe-key'


@task
def migrate_up(c):
    c.run("db-migrate simple-db-migrate.conf")

@task(help={'name': "Name of the migration. should contain only lower case char or _"})
def create_migration(c, name):
    c.run("db-migrate -n {}".format(name))

@task()
def start_dev(c):
    os.environ['FLASK_APP']='app'
    c.run("FLASK_ENV=development flask run")

@task(prepare_test_env, migrate_up)
def test(c):
    c.run("python -m pytest tests -s")

@task(prepare_test_env, migrate_up)
def test_c(c, file_name):
    c.run("python -m pytest {} -s".format(file_name))

@task(prepare_test_env, migrate_up)
def test_f(c, file_name, function_name):
    c.run("python -m pytest {}::{} -s".format(file_name, function_name))

@task
def deploy(c):
    c.run("pip freeze > requirements.txt")
