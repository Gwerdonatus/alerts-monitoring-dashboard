from django.test import TestCase
from django.utils import timezone
from alerts.models import Employee, Alert


class EmployeeModelTest(TestCase):
    def test_employee_str(self):
        employee = Employee.objects.create(
            id="EMP001",
            name="John Doe",
        )
        self.assertEqual(str(employee), "EMP001 - John Doe")


class AlertModelTest(TestCase):
    def test_alert_str(self):
        employee = Employee.objects.create(
            id="EMP001",
            name="Jane Doe",
        )
        alert = Alert.objects.create(
            id="ALT001",
            employee=employee,
            severity=Alert.SEVERITY_HIGH,
            category="Test alert",
            created_at=timezone.now(),
        )
        self.assertIn("ALT001", str(alert))
        self.assertIn("high", str(alert))



