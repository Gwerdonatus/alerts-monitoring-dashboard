from django.core.management.base import BaseCommand
from django.utils import timezone

from alerts.models import Employee, Alert


class Command(BaseCommand):
    help = "Seed initial employees and alerts data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding alert data..."))

        # --- Employees ---
        manager, _ = Employee.objects.get_or_create(
            id="MGR001",
            defaults={
                "name": "Jane Manager",
                "reports_to": None,
            },
        )

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

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))
