hornbook-django
===============

Hornbook using Django

Setup
----
* add 'PROJECT_DIR/libs' to sys.path

edit <strong>djangoappengine/boot.py setup_env()</strong>, add the following before everything else.
<pre><code>
    # add 'PROJECT_DIR/libs' to sys.path
    sys.path.insert(1, os.path.join(PROJECT_DIR, 'libs'))
</code></pre>


Also edit <strong>manage.py</strong>, add the following before everything else.
<pre><code>
    import sys
    import os.path
    sys.path.insert(1, os.path.join(os.path.abspath('.'), 'libs'))
</code></pre>
