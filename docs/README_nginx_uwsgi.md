README_nginx_uwsgi.md
A quick set of notes on how I configured Nginx, uwsgi and Flask

Nginx
=====
I'm using the most recent Nginx which has uwsgi support built-in

`/etc/nginx/conf.d/site.conf`

    location /webmention {
        include uwsgi_params;
        uwsgi_pass    127.0.0.1:5000;
    }

uwsgi
=====
`/etc/uwsgi/apps-enabled/webmentions.ini`

    [uwsgi]
    socket = 127.0.0.1:5000
    wsgi-file = /srv/webmention/basic_listener.py
    manage-script-name = true
    callable = app 
