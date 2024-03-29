# Chapter 3: Pages App

(Content here from Chapter 3 of the book 'Django for Beginners' by William S. Vincent)

## Initial Setup

`RECAP:` Initial setup involves the following steps:
- Make new directory for project named `pages`
- Create virtual environment for project called `.venv` and activate it
- Install Django
- Create new Django project called `django_project`
- Create new Django app called `pages`

**Commands**:

```bash
% mkdir pages
% cd pages
% python3 -m venv .venv
% source .venv/bin/activate
(.venv) % pip install django
(.venv) % django-admin startproject django_project
(.venv) % python manage.py startapp pages
```

Additional steps: Register app: 

- Add `pages` to `INSTALLED_APPS` in `django_project/settings.py`

```python
INSTALLED_APPS = [
    ...,
    'pages.apps.PagesConfig',   # new
]
```

- Migrate the database with `python manage.py migrate`

## Templates

Templates can be used to create the site. Templates contain HTML files with placeholders for logic and dynamic content. Django uses the `Template` class to render templates.

- Where to place the templates? 
    - Option 1: (Default) Django template loader will look within each app for related templates
      Each app needs a `templates` directory, another directory with the name as the app, and then the template files. Which results in the following layout: 

      ```
      └── pages
            └── templates
                └── pages
                    └── home.html
      ``` 
    - Option 2: (Custom) Create a `templates` directory in the project directory and place all templates there, and then use the `DIRS` option in the `TEMPLATES` setting to tell Django where to find the templates. 

The second option is preferred because it allows for a single location for all templates.

Creating the template directory: `mkdir templates` in the project directory.

Updateing the `TEMPLATES` setting in `django_project/settings.py`:

```python

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],  # new
        ...
    },
]
```

## Class-based Views

Function-based views were introduced to deal with repititive tasks. However, they are not very flexible. Class-based views are more flexible and can be used to create more complex views.

Read up more on python classes: https://docs.python.org/3.10/tutorial/classes.html

Using the built in `TemplateView` class to create a view for the home page:

```python
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'home.html'
```

## URLs

The last step is to update the URLs. Updates need to be made in two places: `django_project/urls.py` and `pages/urls.py`.

```python
# django_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # new
]
```

```python
# pages/urls.py

from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
```

## Adding an About Page

Steps: similar to the home page, but with a different template and URL. 

**Step 1:** Create a new template file `about.html` in the `templates/pages` directory.

```html
<!-- templates/about.html -->
<h1>About Page</h1>
```

**Step 2:** Create a new view class `AboutPageView` in `pages/views.py`:

```python
# pages/views.py
...

class AboutPageView(TemplateView):
    template_name = 'about.html'
```

**Step 3:** Update the `pages/urls.py` file:

```python
# pages/urls.py
...

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),  # new
]
```
## Extending Templates

It is possible to extend templates to avoid repetition. For example, we can create a base template that contains the HTML for the header and footer, and then extend it in other templates.

Django has a minimal templating language for adding links and basic logic. Details here: https://docs.djangoproject.com/en/4.0/ref/templates/builtins/#built-in-template-tags-and-filters


## Create a base template

### Adding URL links to the template

The `url` template tag is used to create links to other pages. The `url` tag takes the name of the URL as an argument. For example, since the URL route for our homepage is called `home`, to configure a link to it, the following syntax is syntax is: `{% url 'home' %}`.

```html
<!-- templates/base.html -->
<header>
    <a href = "{% url 'home' %}">Home</a>
    <a href = "{% url 'about' %}">About</a>
</header>

{% block content %}{% endblock content%}
```
At the bottom of the template, the `{% block content %}` tag is used to indicate where the `content` of the page will be inserted. The `{% endblock content %}` tag indicates the end of the block.

### Extending the templates

The `extends` tag is used to extend a template. The `extends` tag takes the name of the template to extend as an argument. For example, to extend the `base.html` template, the following syntax is used: `{% extends 'base.html' %}`.

The `home.html` and `about.html` templates can be updated to extend the `base.html` template:

```html
<!-- templates/home.html -->
{% extends 'base.html' %}

{% block content %}
<h1>Home Page</h1>
{% endblock content %}
```

```html
<!-- templates/about.html -->
{% extends 'base.html' %}

{% block content %}
<h1>About Page</h1>
{% endblock content %}
```

## Tests

"Code without tests is broken by design." - Jacob Kaplan-Moss

Tests are used to ensure that the code is working as expected. Tests are written in the `tests.py` file in each app. There are two types of tests: unit tests and integration tests. Unit tests are used to test individual components of the code, while integration tests are used to test the entire application.

Django's test framework provides some extentsions on top of PYthon's `unittest.TestCase` base class. This includes a `Client` class that can be used to simulate requests to the application and a number of Django-specific assertions. Their are four main test cases - 
- `SimpleTestCase` - used to test views and templates
- `TestCase` - used to test database models
- `TransactionTestCase` - used to test database transactions
- `LiveServerTestCase` - used to test the entire application

In our case, since there is no database involved, we will use the `SimpleTestCase` class. 

### Test 1

Checking if the page is accessible (responds with a 200 status code).

```python
# pages/tests.py
...
class HomePageTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
```
### Test 2

Checking if the page is accessible by URL name. 

```python
# pages/tests.py
...
class HomePageTests(SimpleTestCase):
    ...
    def test_url_available_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
```

### Test 3 

Checking if the correct template is being used: 

```python
# pages/tests.py
...
class HomePageTests(SimpleTestCase):
    ...
    def test_template_name_correct(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
    
    def test_template_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(resonse, '<h1>Hopepage</h1>')

```

# Deploying to Heroku

In order to deploy the app to the cloud, an easy way is to use Heroku. Heroku is a cloud platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

First we need to initialize a git repository in the folder: 

```bash
$ git init
$ git status
$ git add .
$ git commit -m "Initial commit"
```

We can add a github remote to the repository: 

```bash
$ git remote add origin url-to-repo.git
```

Then we need to create an account on Heroku and install the heroku CLI. Installing 
the heroku CLI on mac is easy if we have `brew` installed: 

```bash
$ brew tap heroku/brew && brew install heroku
```

Then we can login to heroku: 

```bash
$ heroku login
```

## Deployment Checklist

Here is a checklist of things to do before deploying the app to Heroku:

- [ ] install `gunicorn`
- [ ] create a `requirements.txt` file
- [ ] update `ALLOWED_HOSTS` in `django_project/settings.py`
- [ ] create a `Procfile`
- [ ] create a `runtime.txt` file

### Install `gunicorn`

Gunicorn is a production-ready web server that can be used to serve Django apps. It is a Python WSGI HTTP server for UNIX. 

```bash
(.venv) > python -m pip install gunicorn==20.1.0
```

### Create a `requirements.txt` file

The `requirements.txt` file contains a list of all the Python packages that are required to run the app. 

```bash
(.venv) > pip freeze > requirements.txt
```

### Update `ALLOWED_HOSTS` in `django_project/settings.py`

The `ALLOWED_HOSTS` setting is used to specify which hosts are allowed to access the app. 

```python
# django_project/settings.py
...
ALLOWED_HOSTS = ["*"]
```

### Create a `Procfile`

The `Procfile` is used to specify the commands that are executed by the app on startup. 

```bash
# Procfile
web: gunicorn django_project.wsgi --log-file -
```

### Create a `runtime.txt` file

The `runtime.txt` file is used to specify the Python version that is used by the app. 

```bash
# runtime.txt
python-3.10.9
```

I actually had an issue with the python runtime version. Had to lookup the version on heroku and use that.

## Deploying to Heroku

Now we can create a new app on Heroku: 

```bash
$ heroku create
```

We can check if the git remotes are set up correctly: 

```bash
$ git remote -v
```

Command to add git remote origin in case anything goes wrong: 

```bash
git remote add heroku https://git.heroku.com/your-app-name.git
```

We need to add some additional heroku configurations, which is to tell Heroku to ignore static files like CSS and JavaScript. 

```bash
$ heroku config:set DISABLE_COLLECTSTATIC=1
```

Also, we need to set the buildpack to Python: 

```bash
$ heroku buildpacks:set heroku/python
```

Now we can push the code to Heroku: 

```bash
$ git push heroku main/master
```

The last step is to make the app live. As websites grow in traffic they need additional Heroku services but for our basic app we can use the free tier. 

```bash
$ heroku ps:scale web=1
```

To open the app in the browser: 

```bash
$ heroku open
```

This app is now live at this URL: https://mysterious-eyrie-32412.herokuapp.com/