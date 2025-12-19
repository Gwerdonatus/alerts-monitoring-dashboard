from django.contrib import admin
from .models import Employee, Alert


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reports_to')
    search_fields = ('id', 'name')


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'severity', 'status', 'created_at')
    list_filter = ('severity', 'status')
    search_fields = ('id', 'employee__name')
