from django.contrib import admin
from .models import Task, Update, Subscriber

admin.site.register(Update)
admin.site.register(Subscriber)

class UpdateInline(admin.TabularInline):
    model = Update

class TaskAdmin(admin.ModelAdmin):
    inlines = [
        UpdateInline,
    ]

admin.site.register(Task, TaskAdmin)
