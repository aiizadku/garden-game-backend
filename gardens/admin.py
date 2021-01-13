from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Plant)
admin.site.register(models.Garden)
admin.site.register(models.Plants_in_garden)
admin.site.register(models.Game)
# admin.site.register(models.User)
