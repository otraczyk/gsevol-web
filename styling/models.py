from __future__ import unicode_literals

from django.db import models

class Option(models.Model):
    """Available options for styling trees.

    This data is constant, at least within app runtime.
    """
    label = models.TextField(max_length=100)
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
    description = models.TextField(max_length=300, default='', blank=True)
    step = models.FloatField(default=1)


    def __str__(self):
        return self.label

    def fix_boolean(self, value):
        if self.type == "bool":
            return bool(int(value))
        return value

    def get_scope(self):
        if self.html_input == 'dropdown':
            verbose = self.verbose_scope.split('/')
            if not self.verbose_scope:
                verbose = self.scope.split(',')
            return zip(self.scope.split(','), verbose)
        elif self.html_input == 'number':
            return self.scope.split('-')
        return []

    def in_scope(self, value):
        if not self.scope:
            return True
        if self.html_input == 'number':
            inf, sup = self.get_scope()
            try:
                return float(value) <= float(sup) and float(value) >= float(inf)
            except ValueError:
                return False
        if self.html_input =="dropdown":
            possible = self.scope.split(',')
            possible = map(self.fix_type, possible)
            return value in possible

    def fix_type(self, value):
        """Cast value to required type. Throws ValueError.
        """
        valid_types = ('float', 'bool', 'int', 'str')
        assert self.type in valid_types
        cast = eval(self.type)
        return cast(value)

    def valid(self, value):
        validations = [
            self.in_scope(value),
        ]
        return all(validations)

    def serialize(self):
        return {
            'label': self.label,
            'name': self.name,
            'input': self.html_input,
            'default': self.fix_boolean(self.default),
            'scope': self.get_scope(),
            'step': self.step,
        }
