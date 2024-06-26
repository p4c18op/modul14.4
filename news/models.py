from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache

class New(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField()
    news = models.ForeignKey(
        to='News',
        on_delete=models.CASCADE,
        related_name='New',
    )

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'new-{self.pk}')

    def __str__(self):
        return f'{self.name.title()}: {self.description}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])


class News(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    news = models.ForeignKey(
        to='News',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

