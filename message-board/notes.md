# Chapter 4: Message Board App 

Initial setup: 

1. make a new directory for our code called `message-board`
2. install Django in a new virtual environment
3. create a new project called `django_project`
4. create a new app called `posts`
5. update `django_project/settings.py`

Commands: 

```bash
% mkdir message-board
% cd message-board
% python3 -m venv .venv
% source .venv/bin/activate
(.venv) % python3 -m pip install django~=4.0.0
(.venv) % django-admin startproject django_project .
(.venv) % python3 manage.py startapp posts
```

Update `django_project/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts.apps.PostsConfig',   # new
]
```

6. Execute the `migrate` command to create the database tables

```bash
(.venv) % python3 manage.py migrate
```

## Create a Database Model

Add a class called `Post` to `posts/models.py`:

```python
# posts/models.py
from django.db import models

class Post(models.Model):
    text = models.TextField()
```

## Activating Models

1. Create a migrations file with `makemigrations`

```bash
(.venv) % python3 manage.py makemigrations
```

2. Build the actual database with the `migrate` command

```bash
(.venv) % python3 manage.py migrate
```

## Create a Superuser

We can create a superuser to access the admin interface:

```bash
(.venv) % python3 manage.py createsuperuser
```

To access the admin interface, run the server and go to `http://localhost:8000/admin/`

## Register the Model with the Admin Interface

1. Open `posts/admin.py`
2. Import the `Post` model

```python
# posts/admin.py 
from django.contrib import admin

from .models import Post

admin.site.register(Post)
```
After this, we can access the admin interface at `http://localhost:8000/admin/` and add new posts.

In order to get a better representation of the post, we can add a `__str__` method to the `Post` class:

```python
# posts/models.py
from django.db import models

class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
```

This displays the first 50 characters of the post in the admin interface.

## Create a View for the Posts

**Step 1**: Create a new view called `HomePageView` in `posts/views.py`:

```python
# posts/views.py
from django.views.generic import ListView
from .models import Post

class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
```

**Step 2**: Create a new template called `home.html` in `templates/posts/`:

```bash
(.venv) % mkdir templates
```
We need to tell Django where to find the templates. Add the following to `django_project/settings.py`:

```python
# django_project/settings.py
TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR / 'templates')],   # new
        ...
    },
]
```

Content of `home.html`:

```html
<!-- templates/posts/home.html -->
<h1>Message board homepage</h1>
<ul>
    {% for post in post_list %}
        <li> {{ post.text }}</li>
    {% endfor %}
</ul>
```

**Step 3**: Add a URLS for the view

Add ULR in `django_project/urls.py`:

```python
# django_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]
```

Create a new file called `urls.py` in `posts/`:

```python
# posts/urls.py
from django.urls import path
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
]
```

## Tests

Create a new testing class called `PostTests` in `posts/tests.py` and test 
if the model is created correctly:

```python
# posts/tests.py

from django.test import TestCase

from .models import Post

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(text = "This is a test!")
    
    def test_model_content(self):
        self.assertEqual(self.post.text, "This is a test!")

```

Add More tests: 

- Test if the URL exists at the correct location
- Test if the URL name is correct 
- Test if the view uses the correct template
- Test if the template contains the correct content

```python
# posts/tests.py

...

class PostTests(TestCase):

    ...

    def test_url_exists_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_name_correct(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')
    
    def test_template_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "This is a test!")
``` 

The last three tests can be combined into one test: 

```python
# posts/tests.py

...

class PostTests(TestCase):

    ...

    def test_view_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "This is a test!")
```

To run the tests, execute the following command:

```bash
(.venv) % python3 manage.py test
```

## Deploying in Heroku

- Initialize Git Repository

```bash
(.venv) % git init
(.venv) % git add .
(.venv) % git commit -m "Initial commit"
```

Checklist: 

- [ ] install `gunicorn`
- [ ] create a `requirements.txt` file
- [ ] update `ALLOWED_HOSTS` in `django_project/settings.py`
- [ ] create a `Procfile`
- [ ] create a `runtime.txt`

Install `gunicorn`:
```bash
(.venv) % python -m pip install gunicorn==20.0.1
(.venv) % pip3 freeze > requirements.txt
```

Add the following to `django_project/settings.py`:

```python
# django_project/settings.py
...
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
...
```
-> This is better than using the wildcard `*` because it is more secure.
-> This allows only the hosts specified in the list to access the application.

Create `Procfile`:
```bash
# Procfile
web: gunicorn django_project.wsgi --log-file -
```

Create `runtime.txt`:
```bash
# runtime.txt
python-3.10.9
```

## Heroku Deployment:

- make sure the Heroku CLI is installed and logged-in
- create a new Heroku app

    ```bash
    (.venv) % heroku create
    ```
- Disable static collection: 

    ```bash
    (.venv) % heroku config:set DISABLE_COLLECTSTATIC=1
    ```

- push the code to Heroku

    ```bash
    (.venv) % git push heroku main/master
    ```

- Scaling the dynos:

    ```bash
    (.venv) % heroku ps:scale web=1
    ```

The heroku app is now live at: https://sleepy-coast-49587.herokuapp.com/