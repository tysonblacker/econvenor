# eConvenor

[eConvenor](https://www.econvenor.org) is Django web application which helps people convene a group more effectively.

## Installation for local testing or development

1. Clone the eConvenor Github repository.
1. Set up a new virtual environment.
1. Install `requirements.txt`.
1. Set these environment variables in `.bashrc` (DO NOT use these values for PRODUCTION):
    - ECONVENOR_SECRET_KEY=13480dj3io12nrb4786ydge76gq78yd3b
    - ECONVENOR_HOST_NAME=no_host
    - ECONVENOR_EMAIL_PORT=no_port
    - ECONVENOR_DATABASE_NAME=econvenor_database
    - ECONVENOR_DATABASE_PASSWORD=ncds8rbce7
    - ECONVENOR_DATABASE_USER=eonvenor_database_owner
    - ECONVENOR_EMAIL_PASSWORD=no_email_password
    - ECONVENOR_ADMIN_URL=admin
1. Run `manage.py syncdb`. During this process, set up a superuser with account name `superuser`, email `superuser@econvenor.org` and password `superuser`
1. Run `manage.py migrate`.
1. Run `manage.py loaddata testdata`. This sets up a user with email `ash@econvenor.org` and password `ashanderson1!` and populates that account with test data.

## Licence

Details coming soon.