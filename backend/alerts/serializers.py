from rest_framework import serializers
from .models import Employee, Alert


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Minimal employee representation for alert context.
    """

    class Meta:
        model = Employee
        fields = ("id", "name")


class AlertSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for alerts.
    """

    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = (
            "id",
            "employee",
            "severity",
            "category",
            "status",
            "created_at",
        )
        read_only_fields = fields
