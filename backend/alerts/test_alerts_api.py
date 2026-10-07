from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from alerts.models import Employee, Alert


class AlertAPITestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="manager")
        self.manager = Employee.objects.create(
            id="MGR001",
            name="Jane Manager",
            user=self.user,
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
        self.client.force_authenticate(self.user)

    def test_list_alerts_success(self):
        """
        Senior-level test:
        - Verifies correct HTTP status
        - Verifies response structure
        - Verifies data integrity
        """
        url = reverse("alerts:list")
        response = self.client.get(url)

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
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"], [])
        self.assertEqual(response.data["count"], 0)

    def test_anonymous_requests_are_rejected(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("alerts:list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_authentication_flow(self):
        token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=None)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        response = self.client.get(reverse("alerts:list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_manager_id_query_cannot_impersonate_another_manager(self):
        other_manager = Employee.objects.create(id="MGR002", name="Other Manager")
        other_employee = Employee.objects.create(
            id="EMP002", name="Other Employee", reports_to=other_manager
        )
        Alert.objects.create(
            id="ALT002",
            employee=other_employee,
            severity=Alert.SEVERITY_HIGH,
            category="Private alert",
            created_at=timezone.now(),
        )

        response = self.client.get(reverse("alerts:list"), {"manager_id": "MGR002"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data["results"]], ["ALT001"])

    def test_manager_cannot_dismiss_alert_outside_their_subtree(self):
        outsider = Employee.objects.create(id="EMP999", name="Outsider")
        foreign_alert = Alert.objects.create(
            id="ALT999",
            employee=outsider,
            severity=Alert.SEVERITY_HIGH,
            category="Restricted",
            created_at=timezone.now(),
        )

        response = self.client.post(reverse("alerts:dismiss", args=[foreign_alert.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        foreign_alert.refresh_from_db()
        self.assertEqual(foreign_alert.status, Alert.STATUS_OPEN)

    def test_manager_can_dismiss_descendant_alert_idempotently(self):
        url = reverse("alerts:dismiss", args=[self.alert.id])
        first = self.client.post(url)
        second = self.client.post(url)

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(second.data["status"], Alert.STATUS_DISMISSED)

    def test_invalid_scope_returns_bad_request(self):
        response = self.client.get(reverse("alerts:list"), {"scope": "company"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_filter_returns_field_error(self):
        response = self.client.get(reverse("alerts:list"), {"severity": "critical"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("severity", response.data)

    def test_filters_can_be_combined(self):
        response = self.client.get(
            reverse("alerts:list"),
            {"severity": "high", "status": "open", "q": "Gwer"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_subtree_scope_includes_nested_reports(self):
        nested = Employee.objects.create(
            id="EMP002", name="Nested Employee", reports_to=self.employee
        )
        Alert.objects.create(
            id="ALT002",
            employee=nested,
            severity=Alert.SEVERITY_LOW,
            category="Nested alert",
            created_at=timezone.now(),
        )

        direct = self.client.get(reverse("alerts:list"), {"scope": "direct"})
        subtree = self.client.get(reverse("alerts:list"), {"scope": "subtree"})

        self.assertEqual(direct.data["count"], 1)
        self.assertEqual(subtree.data["count"], 2)

    def test_pagination_is_bounded_and_navigable(self):
        Alert.objects.bulk_create(
            [
                Alert(
                    id=f"PAGE{index:03d}",
                    employee=self.employee,
                    severity=Alert.SEVERITY_LOW,
                    category="Pagination",
                    created_at=timezone.now(),
                )
                for index in range(55)
            ]
        )

        first = self.client.get(reverse("alerts:list"), {"page_size": 100})
        second = self.client.get(reverse("alerts:list"), {"page_size": 50, "page": 2})

        self.assertEqual(first.data["count"], 56)
        self.assertEqual(len(first.data["results"]), 50)
        self.assertIsNotNone(first.data["next"])
        self.assertEqual(len(second.data["results"]), 6)
