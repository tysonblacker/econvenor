eConvenor
=========

eConvenor is the `Django-based <https://djangoproject.com>`_ web app which
powers the `eConvenor <https://econvenor.org>`_ web service.

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

These instructions are written for Ubuntu Linux. If you're running a different
operating system, you will probably need to adjust them.

When you see text following a ``$`` symbol in grey box, type or paste it
into a terminal window, then press ``Enter``.

Step 1. Install pip, virtualenv and virtualenvwrapper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have these set up, skip to Step 2.

Install pip::

    $ sudo apt-get install python-pip

Install virtualenv and virtualenvwrapper::

    $ sudo pip install virtualenv virtualenvwrapper

Open ``~/.bashrc``:: 

    $ nano ~/.bashrc

Add these lines to the end of ``~/.bashrc``, then save and close it::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Projects
    source /usr/local/bin/virtualenvwrapper.sh

Reload ``~/.bashrc``::

    $ source ~/.bashrc

Step 2. Set up a virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a virtualenv for your eConvenor development environment::

    $ mkvirtualenv econvenor

Open ``~/.virtualenvs/econvenor/bin/postactivate``::

    $ nano ~/.virtualenvs/econvenor/bin/postactivate

Add these lines to the end of ``~/.virtualenvs/econvenor/bin/postactivate``,
then save and close it::

    export ECONVENOR_ADMIN_URL=administration
    export ECONVENOR_DATABASE_NAME=econvenor_database
    export ECONVENOR_DATABASE_PASSWORD=ncds8rbce7
    export ECONVENOR_DATABASE_USER=eonvenor_database_owner
    export ECONVENOR_EMAIL_PASSWORD=no_email_password
    export ECONVENOR_EMAIL_PORT=no_port
    export ECONVENOR_ENVIRONMENT=development
    export ECONVENOR_SECRET_KEY=13480dj3io12nrb4786ydge76gq78yd3b

Now we need to restart the virtualenv so that these setting take effect. First,
deactivate the virtualenv::

    $ deactivate

Now re-start the virtualenv::

    $ workon econvenor

Step 3. Clone the repo
^^^^^^^^^^^^^^^^^^^^^^

For these instructions we'll clone this repo to ``~/Projects/econvenor``, but
you can put the eConvenor code anywhere you like.

Make the ``~/Projects/econvenor`` directory::

    $ mkdir -p ~/Projects/econvenor
 
Then open it::

    $ cd ~/Projects/econvenor

You'll need to have Git installed. If you don't have it installed, install it
now::

    $ sudo apt-get install git

Clone the repo to your computer::
 
    $ git clone https://github.com/econvenor/econvenor.git

Step 4. Install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install some system-wide dependencies which will be needed::

    $ sudo apt-get install python-dev postgresql libpq-dev

Go to the directory which contains ``requirements.txt``::

    $ cd ~/Projects/econvenor/econvenor

Install the required Python packages in your virtualenv::

    $ pip install -r requirements.txt


Step 5. Set up the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Initialise the database::

    $ python manage.py syncdb

As the database is being created you'll be prompted to set up a superuser. Do
so with account name ``superuser``, email ``superuser@econvenor.org`` and
password ``superuser``.

Migrate the database::

  $ python manage.py migrate
  
Load the example data::

  $ python manage.py loaddata testdata

This has set up a user with email ``ash@econvenor.org`` and password
``ashanderson1!`` and populated that account with test data.
    
Step 6. Create a directory for user content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create the directory which will contain user-generated content::

    $ mkdir -p ~/Projects/econvenor/econvenor/media

That's it! You should now have a complete eConvenor instance which is ready to
be started!


Starting the development instance
---------------------------------

Once you've set up a development instance, the commands below will start
it up anytime.

Start the virtualenv::

    $ workon econvenor

Go to the directory which contains eConvenor's ``manage.py`` file::

    $ cd ~/Projects/econvenor/econvenor

Start the development server::

    $ python manage.py runserver

Now point your browser to ``localhost:8000`` and the site will load. You can
sign in to eConvenor as ``ash@econvenor.org`` with the password
``ashanderson1!``.
