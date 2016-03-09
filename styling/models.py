from __future__ import unicode_literals

from django.db import models

class Option(models.Model):
    """Available options for styling trees.

    This data is constant, at least within app runtime.
    """
    label = models.CharField(max_length=100)
    name = models.CharField(max_length=100, db_index=True)
    gene = models.BooleanField(default=False)
    species = models.BooleanField(default=False)
    mapping = models.BooleanField(default=False)
    scenario = models.BooleanField(default=False)
    diagram = models.BooleanField(default=False)
    unrooted = models.BooleanField(default=False)
    html_input = models.CharField(max_length=100)
    scope = models.CharField(max_length=100, default='', blank=True)
    verbose_scope = models.CharField(max_length=100, default='', blank=True)
    type = models.CharField(max_length=100)
    default = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default='', blank=True)


    def __str__(self):
        return self.label

    def fix_boolean(self, value):
        if self.type == "bool":
            return bool(int(value))
        return value

    def serialize(self):
        return {
            'label': self.label,
            'name': self.name,
            'input': self.html_input,
            'default': self.fix_boolean(self.default),
        }
