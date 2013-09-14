hornbook-django
===============

Hornbook using Django

Setup
----
* add 'PROJECT_DIR/libs' to sys.path

edit <strong>djangoappengine/boot.py setup_env()</strong>, add
<pre><code>
    # add 'PROJECT_DIR/libs' to sys.path
    sys.path.insert(1, os.path.join(PROJECT_DIR, 'libs'))
</code></pre>
before everything else.
