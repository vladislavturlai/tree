from django.db import models


class Category(models.Model):
    name = models.TextField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return f'{self.name}'
