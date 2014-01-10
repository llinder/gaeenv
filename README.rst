Google App Engine virtual environment
===========================

``gaeenv`` (Google App Engine virtual environment) is a tool to integrate
Google App Engine SDK into existing environments built by virtualenv_

Install
-------

Global installation
^^^^^^^^^^^^^^^^^^^

You can install gaeenv globally with `easy_install`_::

    $ sudo easy_install gaeenv

or `pip`_::

    $ sudo pip install gaeenv

Local installation
^^^^^^^^^^^^^^^^^^

Using virtualenv_ you can install gaeenv via pip_/easy_install_ inside any 
virtual environment built with virtualenv_ or virtualenv_wrapper_::

    $ virtualenv --no-site-packages env
    $ . env/bin/activate
    (env) $ pip install gaeenv
    (env) $ gaeenv --version
    0.1.0

If you want to work with the latest version of the gaeenv you can 
install it from the github `repository`_::

    $ git clone https://github.com/llinder/gaeenv.git
    $ ./gaeenv/gaeenv/main.py --help

.. _repository: https://github.com/llinder/gaeenv
.. _pip: http://pypi.python.org/pypi/pip
.. _easy_install: http://pypi.python.org/pypi/setuptools


Dependency
----------

For gaeenv
^^^^^^^^^^^

* python
* requests

Usage
-----

Basic
^^^^^

Activate existing environment::

    $ . env/bin/activate

Or activate existing environment with virtualenvwrapper::

    $ workon env

Install latest Google App Engine SDK into environment::

    (env) $ gaeenv install sdk

Check location of main utilities::

    (env) $ which dev_appserver.py
    VIRTUAL_ENV/lib/google_appengine/dev_appserver.py

    (env) $ which appcfg.py
    VIRTUAL_ENV/lib/google_appengine/appcfg.py

Deactivate environment::

    (env) $ deactivate_gae

Advanced
^^^^^^^^

Get available SDK versions::

    $ gaeenv list sdk
    1.8.8
    1.8.7
    1.8.6
    1.8.5
    1.8.4
    1.8.3
    1.8.2
    1.8.1
    1.8.0
    1.7.7
    1.7.6
    1.7.5
    1.7.4    

Install App Engine SDK "1.8.1"::

    $ gaeenv install sdk --version=1.8.1

Link all packages in requirements.txt into src/lib::

    $ . env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ gaeenv install requirements -r requirements.txt
