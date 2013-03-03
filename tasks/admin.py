from django.contrib import admin
from .models import Task, Update, Recipient

admin.site.register(Update)
admin.site.register(Recipient)

class UpdateInline(admin.TabularInline):
    model = Update

class RecipientInline(admin.TabularInline):
    model = Recipient

class TaskAdmin(admin.ModelAdmin):
    inlines = [
        UpdateInline,
        RecipientInline,
    ]

admin.site.register(Task, TaskAdmin)
