from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from alerts.models import Employee, Alert


class Command(BaseCommand):
    help = "Seed initial employees and alerts data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding alert data..."))

        user, user_created = get_user_model().objects.get_or_create(
            username="demo-manager"
        )
        if user_created:
            user.set_unusable_password()
            user.save(update_fields=["password"])

        # --- Employees ---
        manager, _ = Employee.objects.get_or_create(
            id="MGR001",
            defaults={
                "name": "Jane Manager",
                "reports_to": None,
            },
        )
        if manager.user_id != user.id:
            manager.user = user
            manager.save(update_fields=["user"])

        employee1, _ = Employee.objects.get_or_create(
            id="EMP002",
            defaults={
                "name": "John Employee",
                "reports_to": manager,
            },
        )

        employee2, _ = Employee.objects.get_or_create(
            id="EMP003",
            defaults={
                "name": "Sarah Employee",
                "reports_to": manager,
            },
        )

        # --- Alerts ---
        Alert.objects.get_or_create(
            id="ALT001",
            defaults={
                "employee": employee1,
                "severity": Alert.SEVERITY_HIGH,
                "category": "Missed check-in",
                "created_at": timezone.now(),
                "status": Alert.STATUS_OPEN,
            },
        )

        Alert.objects.get_or_create(
            id="ALT002",
            defaults={
                "employee": employee2,
                "severity": Alert.SEVERITY_MEDIUM,
                "category": "Performance alert",
                "created_at": timezone.now(),
                "status": Alert.STATUS_OPEN,
            },
        )

        token, _ = Token.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
        self.stdout.write(f"Demo API token: {token.key}")
