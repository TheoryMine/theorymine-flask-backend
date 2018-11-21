#theorymine backend in flask

to install libraries:

pip install -r requirements.txt

to migrate up:

mysql database.
set env variables: DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
then run: 
inv migrate-up

to run:

set env valiables : DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, SECRET_KEY, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY


then run: 
inv start-dev


to test: 

set env variables: DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME
then run:
inv test


