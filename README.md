hornbook-django
===============

Hornbook using Django

Setup
----
* add 'PROJECT_DIR/libs' to sys.path

edit <strong>djangoappengine/boot.py setup_env()</strong>, add the following before everything else.
<pre><code>
    # add 'PROJECT_DIR/libs' and 'PROJECT_DIR/utils' to sys.path
    sys.path.insert(1, os.path.join(PROJECT_DIR, 'libs'))
    sys.path.insert(1, os.path.join(PROJECT_DIR, 'utils'))
</code></pre>

Also edit <strong>manage.py</strong>, add the following before everything else.
<pre><code>
    import sys
    import os.path
    sys.path.insert(1, os.path.join(os.path.abspath('.'), 'libs'))
</code></pre>

Development Server
----
<pre><code>
	pytho manage.py runserver
</code></pre>
Then visit: localhost:8000


Url mapping
----
Use GAE app.yaml setting to contrl basic static files Url mapping
  /favicon.ico
  /js
  /css

Use Django urls.py to contrl web service Url mapping, and templates
  /accounts/login
  /admin/
  /hornbook_api/


Plain data structure
----
Character and word are unified to the concept of Vocabulary, which is a plain string holding unicode chars. This plain data structure is transferred between JavaScript methods, as well as web services.
