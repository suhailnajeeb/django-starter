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

### Test 1: Checking if the two URLs are returning HTTP 200 status code which is the standard response for a successful HTTP request

```python
# pages/tests.py

from django.test import SimpleTestCase

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
```

**Running Tests:** `python manage.py test`

If you see an error such as `AssertionError: 301 != 200` it’s likely you forgot to add the trailing slash to `"/about"` above. The web browser knows to automatically add a slash if it’s not provided, but that causes a `301` redirect, not a `200` success response!

