from django.db import models

# Create your models here.

class Post(models.Model):
    text = models.TextField()

    def __str__(self):
        """A String representation of the mode."""
        return self.text[:50]