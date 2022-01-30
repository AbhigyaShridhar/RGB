from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import id_generator

# Create your models here.
class User(AbstractUser):
    identifier = models.CharField(unique=True, blank=False, null=True, max_length=10)
    score = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    items = models.ManyToManyField("Item", blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['-score', '-red', '-blue', '-green']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = id_generator()
            while User.objects.filter(identifier=self.identifier).exists():
                self.identifier = id_generator()
        super(User, self).save(*args, **kwargs)

class Item(models.Model):
    name = models.CharField(max_length=20, null=True, blank=False)
    value = models.IntegerField(default=10)
    stock = models.IntegerField(default=5)
    description = models.TextField()
    image = models.URLField(null=True, blank=False)

    class ColorChoices(models.TextChoices):
        RED = 'RED'
        BLUE = 'BLUE'
        GREEN = 'GREEN'

    color = models.CharField(
        max_length=5,
        choices=ColorChoices.choices,
        default=ColorChoices.RED,
    )

    class Meta:
        ordering = ['-value']

    def __str__(self):
        return self.name
