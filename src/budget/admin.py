from django.contrib import admin

# Register your models here.
from .models import Project, Expense, Category

admin.site.register(Project)
admin.site.register(Expense)
admin.site.register(Category)
