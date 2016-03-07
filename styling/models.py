from __future__ import unicode_literals

from django.db import models

class Option(models.Model):
    label = models.CharField(max_length=100)
    name = models.CharField(max_length=100, db_index=True)
    gene = models.BooleanField(default=False)
    species = models.BooleanField(default=False)
    mapping = models.BooleanField(default=False)
    embedding = models.BooleanField(default=False)
    diagram = models.BooleanField(default=False)
    html_input = models.CharField(max_length=100)
    scope = models.CharField(max_length=100, default='', blank=True)
    verbose_scope = models.CharField(max_length=100, default='', blank=True)
    type = models.CharField(max_length=100)
    default = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default='', blank=True)


    def __str__(self):
        return self.label

    def serialize(self):
        return {
            'label': self.label,
            'name': self.name,
            'input': self.html_input,
            'default': self.default,
        }
