from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Calendar)
admin.site.register(Inventory)
admin.site.register(Note)
admin.site.register(Team)
admin.site.register(Role)
admin.site.register(FileManager)
admin.site.register(Objective)