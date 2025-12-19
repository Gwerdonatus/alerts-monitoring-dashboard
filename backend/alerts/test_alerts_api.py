from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from alerts.models import Employee, Alert


class AlertAPITestCase(APITestCase):
    def setUp(self):
        self.manager = Employee.objects.create(
            id="MGR001",
            name="Jane Manager",
        )

        self.employee = Employee.objects.create(
            id="EMP001",
            name="Gwer Employee",
            reports_to=self.manager,
        )

        self.alert = Alert.objects.create(
            id="ALT001",
            employee=self.employee,
            severity=Alert.SEVERITY_HIGH,
            category="Test alert message",
            created_at=timezone.now(),
        )

    def test_list_alerts_success(self):
        """
        Senior-level test:
        - Verifies correct HTTP status
        - Verifies response structure
        - Verifies data integrity
        """
        url = reverse("alerts:list")
        response = self.client.get(url, {'manager_id': self.manager.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertEqual(len(response.data["results"]), 1)

        alert = response.data["results"][0]
        self.assertEqual(alert["employee"]["id"], self.employee.id)
        self.assertEqual(alert["employee"]["name"], self.employee.name)
        self.assertEqual(alert["category"], self.alert.category)

    def test_alerts_empty_response(self):
        """
        Edge case:
        - No alerts exist
        - API should return empty list, not error
        """
        Alert.objects.all().delete()

        url = reverse("alerts:list")
        response = self.client.get(url, {'manager_id': self.manager.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.data["count"], 0)


