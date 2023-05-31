from django.db import models
from django.urls import reverse


class Contact(models.Model):
    # Форма подписки на Email
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('home')


    def __str__(self):
        return self.email