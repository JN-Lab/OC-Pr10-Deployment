# OC-Pr10-Deployment
Repository for Project 10 from Openclassrooms cursus in Software Development

## Project Description

This is a web application built with **Django** to help user to find healthier products of their favorites food.
The objective of this project is to deploy the application from project8 on **Digital Ocean** server.

### Simplified App Structure

```
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- manage.py
|-- Procfile
|-- geckodriver.log
|-- purbeurre_platform/
    |-- __init__.py
    |-- settings/
        |-- __init__.py
        |-- travis.py
        |-- production.py (not committed)
    |-- urls.py
    |-- wsgi.py
    |-- static/s
|-- search/
    |-- __init__.py
    |-- dumps/
    |-- management/
    |-- migrations/
    |-- static/
    |-- templates/
    |-- utils/
    |-- tests/
    |-- admin.py
    |-- apps.py
    |-- forms.py
    |-- models.py
    |-- urls.py
    |-- views.py
|-- static/
    |-- boostrap/
    |-- css/
    |-- scss/
    |-- jquery/
    |-- js/
    |-- magnific-popup/
|-- templates/
    |-- 404.html
    |-- 500.html
    |-- base.html
    |-- legal.html
```

## Built With
* Django
* psycopg2
* requests

## Elements used for deployment
* Travis
* Nginx
* Gunicorn
* Supervisor
* Sentry
* Git