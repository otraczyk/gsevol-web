from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from styling.models import Option


class OptionAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        """Hacked to display options list as index page.
        """
        option_admin = self._registry[Option]
        option_response = option_admin.changelist_view(request, extra_context)

        return option_response

admin_site = OptionAdminSite(name='site')


class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'type', 'default', 'unrooted', 'gene',
                     'species', 'scenario', 'diagram', 'mapping', 'html_input',
                     'description')
    list_filter = ('unrooted', 'scenario', 'diagram', 'mapping', 'gene')
    list_editable = ('unrooted', 'scenario', 'default', 'type', 'label',
                     'diagram', 'mapping', 'gene', 'html_input', 'species',
                     'description')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'5'})},
        models.TextField: {'widget': TextInput(attrs={'size':'18'})},
    }

admin_site.register(Option, OptionAdmin)
