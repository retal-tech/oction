from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Projects, Contact

admin.site.register(Projects, TranslatableAdmin)
admin.site.register(Contact)
