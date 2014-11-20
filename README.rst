eConvenor
=========

eConvenor is the Django web app which powers the
`eConvenor <https://econvenor.org>`_ web service.

eConvenor helps progressive campaigns and organisations be more effective.

|

.. image:: https://econvenor.org/static/images/landing/agendas-screenshot-1-large.png
   :alt: eConvenor screenshot

|

Help out!
---------

If you're interested in contributing to eConvenor, check out our
`volunteering <https://econvenor.org/volunteer>`_ page.

If you want to be a part of the project, there's plenty to do. Take your pick
from anything on our `issue tracker <https://trac.econvenor.org>`_!


Setting up a development instance
---------------------------------

Step 1. Install pip, virtualenv and virtualenvwrapper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have these set up, skip to Step 2.

::

    sudo apt-get install python-pip
    sudo pip install virtualenv virtualenvwrapper

Add these lines to the end of your ``~/.bashrc`` file:

::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Projects
    source /usr/local/bin/virtualenvwrapper.sh

Reload ``~/.bashrc``:

::

    source ~/.bashrc

Step 2. Set up a virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    mkvirtualenv econvenor

Add these lines to the end of ``~/.virtualenvs/econvenor/bin/postactivate``:

::

    export ECONVENOR_ADMIN_URL=administration
    export ECONVENOR_DATABASE_NAME=econvenor_database
    export ECONVENOR_DATABASE_PASSWORD=ncds8rbce7
    export ECONVENOR_DATABASE_USER=eonvenor_database_owner
    export ECONVENOR_EMAIL_PASSWORD=no_email_password
    export ECONVENOR_EMAIL_PORT=no_port
    export ECONVENOR_ENVIRONMENT=development
    export ECONVENOR_SECRET_KEY=13480dj3io12nrb4786ydge76gq78yd3b


Restart the virtualenv so that these setting take effect:

::

    deactivate
    workon econvenor

Step 3. Clone the repo
^^^^^^^^^^^^^^^^^^^^^^

For these instructions we'll clone the repo to ``~/Projects/econvenor``, but you
can put it anywhere you like.

::

    mkdir -p ~/Projects/econvenor
    cd ~/Projects/econvenor
    git clone https://github.com/econvenor/econvenor.git

Step 4. Install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    cd ~/Projects/econvenor
    pip install -r requirements.txt

If the above fails, repeat this step after installing dependencies with the
following command:

::

    sudo apt-get install python-dev postgresql libpq-dev

Step 5. Set up the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initialise the database:

::

    python manage.py syncdb

You'll be prompted to set up a superuser. Do so with account name ``superuser``,
email ``superuser@econvenor.org`` and password ``superuser``.

Migrate the database:

::

  python manage.py migrate
  
Load test data from fixtures:

::

  python manage.py loaddata testdata

This has set up a user with email `ash@econvenor.org` and password
`ashanderson1!` and populated that account with test data.
    
Step 6. Create a directory for user content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    mkdir -p ~/Projects/econvenor/econvenor/media

Step 7. Start eConvenor and log in
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start the server:

::

    python manage.py runserver

Now browse to ``localhost:8000`` and sign in as ``ash@econvenor.org`` with the
password ``ashanderson1!``.

You're done!
