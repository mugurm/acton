from django.contrib import admin
from .models import Task, Update, Receipt

admin.site.register(Update)
admin.site.register(Receipt)

class UpdateInline(admin.TabularInline):
    model = Update

class ReceiptInline(admin.TabularInline):
    model = Receipt

class TaskAdmin(admin.ModelAdmin):
    inlines = [
        UpdateInline,
        ReceiptInline,
    ]

admin.site.register(Task, TaskAdmin)
