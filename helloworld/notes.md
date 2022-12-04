Content from Chapter 2 of Django for Beginners from W. Vincent

## Initial Setup

Setting up a virtual environment named `.venv` :  
```
% python3 -m venv .venv
```
Activating the environment named `.venv`:  
```
% source .venv/bin/activate
```
Creating a project named `django_project` in the root folder (`.`) using the 
command `startproject`:  

```
(.venv) > django-admin startproject django_project .
```

## Directory Structure

The directory structure of the project is as follows:  
```
.
├── django_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── .venv/
```



* `__init__.py` : empty file that tells Python that this directory should be
considered a Python package.
* `asgi.py` : entry point for ASGI-compatible web servers to serve your project.
* `settings.py` : settings/configuration for this Django project.
* `urls.py` : the URL declarations for this Django project; a “table of contents”
of your Django-powered site.
* `wsgi.py` : entry point for WSGI-compatible web servers to serve your project.


Running the Development Server

```
(.venv) > python manage.py runserver
```

Migrating the Database (although not relevant for this project)

```
(.venv) > python manage.py migrate
```

## HTTP Request/Response Cycle

HTTP - Hyper Text Transfer Protocol - Tim Berners-Lee (1989)

The HTTP Request/Response Cycle for Django looks like -

```
HTTP Request -> URL -> Django combines database, logic, styling -> HTTP Response
```

## Model-View-Controller vs Model-View-Template

Traditional web frameworks use the *Model-View-Controller (MVC)* pattern which has
three components - Model, View, Controller.

* Model - the data layer
* View - the presentation layer
* Controller - the logic layer

Django uses the *Model-View-Template (MVT)* pattern which has three components Model, View, Template and an additional component - URLconf.

* Model - the data layer
* View - the presentation layer
* Template - presents the data as HTML with optional styling
* URLconf - Regular Expressions that map URLs to Views

## The complete Django flow

```
HTTP Request -> URL -> View -> Model and Template -> HTTP Response
```

## Apps

Django uses apps to organize the project. An app is a collection of related models, views, templates, and other files. A project can have multiple apps.

## Creating an App

Creating an app named `pages` in the project `django_project`:

```
(.venv) > python manage.py startapp pages
```
The directory structure of the app `pages` looks like - 
    
```
pages
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

Different components of the app `pages`:

* `admin.py` - configuration file for the Django Admin app
* `apps.py` - configuration file for the app
* `migration` - directory for database migrations
* `models.py` - database models
* `tests.py` - unit tests
* `views.py` - views (request/response logic)

## Registering the App

Registering the app `pages` in the project `django_project`:

```python
# django_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages.apps.PagesConfig',   # <-- add this line
]
```

## Basics 

Four separate files are used to create a dynamic web page in Django:

* `models.py`
* `views.py`
* `template.html`
* `urls.py`

To create a static webpage, we can hardcode the data into a view, which we will
be doing for now. 

## Creating a View

Creating a view named `homePageView` in the app `pages`:

```python
# pages/views.py

from django.http import HttpResponse

def homePageView(request):
    return HttpResponse('Hello, World!')
```
This is an example of an FBV (Function Based View).

## Types of Django Views

There are mainly two types of views in Django:
- **Function Based Views (FBVs)**
- **Class Based Views (CBVs)**

There is also a number of built in **Generic Class-Based Views (GCBVs)** that are 
used to handle common tasks. 


## Adding a URL

Adding a URL named `home` in the app `pages`:

```python
# pages/urls.py

from django.urls import path
from .views import homePageView

urlpatterns = [
    path('', homePageView, name='home'),
]
```

Any URL Pattern has three parts - 
* **String Pattern** - the URL pattern to match (e.g. `''` for the homepage)
* **View** - the view function to call when Django finds a match (`homePageView`)
* **name** - opotional named URL pattern called `'home'`

## Add URL to Project

Include the URL patterns from the app `pages` in the project `django_project`:

```python
# django_project/urls.py

from django.contrib import admin
from django.urls import path, include   # <-- add include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),    # <-- add this line
]
```