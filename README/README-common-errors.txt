Some tips to run the flask server on Ubuntu 22.04.1 LTS with Python 3.10.4:


1) python staas_site.py: errors in MarkupSafe, Pillow, cffi  required me to update requirements.txt with the following changes

        < cffi==1.15.1
        > cffi==1.11.5

        < MarkupSafe==1.1.1
        > MarkupSafe==1.0

        < Werkzeug==0.16.1
        > Werkzeug==0.14.1

2) Also needed to change the following collections imports to collections.abc:

  File /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/jinja2/tests.py, line 13, in <module>
    from collections import Mapping
  ImportError: cannot import name 'Mapping' from 'collections' (/usr/lib/python3.10/collections/__init__.py)

  File /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/flask/sessions.py, line 14, in <module>
    from collections import MutableMapping
  ImportError: cannot import name 'MutableMapping' from 'collections' (/usr/lib/python3.10/collections/__init__.py)

  File /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/sqlalchemy/sql/base.py, line 49, in <module>
    class _DialectArgView(collections.MutableMapping):
  AttributeError: module 'collections' has no attribute 'MutableMapping'

  File /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/sqlalchemy/sql/base.py, line 102, in <module>
    class _DialectArgDict(collections.MutableMapping):
  AttributeError: module 'collections' has no attribute 'MutableMapping'

  File /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/sqlalchemy/util/_collections.py, line 798, in to_list
    if not isinstance(x, collections.Iterable) or AttributeError: module 'collections' has no attribute 'Iterable'

Example of a fix:
    >from collections import Mapping
    >if not isinstance(x, collectionsIterable)        Error: module 'collections' has no attribute 'Iterable'

    <from collections.abc import Mapping
    <if not isinstance(x, collections.abc.Iterable)

3) staas_site.py: run on port 7000 any interface
        #app.run(debug=True)                                 to run local browser with http://127.0.0.1:5000/
        app.run(debug=True, port=7000, host="0.0.0.0" )    # to run on specified port 7000 on any interface

   An alternate way to startup inside the virtual environment is:
       export FLASK_APP=staas_site.py
       export FLASK_ENV=development
       flask run -h 0.0.0.0 -p 8000

4) Deprecation warning bypassed:
        /home/jtb/PycharmProjects/STAAS-Web-App/venv/lib/python3.10/site-packages/flask_sqlalchemy/__init__.py:793:
        FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.
        Set it to True or False to suppress this warning.

  Changed this:
        track_modifications = app.config.setdefault(
#            'SQLALCHEMY_TRACK_MODIFICATIONS', None
            'SQLALCHEMY_TRACK_MODIFICATIONS', False
        )
