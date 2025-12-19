from django.db import models


class Employee(models.Model):
    """
    Represents an employee in the org chart.
    Self-referential relationship allows tree/graph traversal.
    """
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=255)
    reports_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='direct_reports'
    )

    class Meta:
        indexes = [
            models.Index(fields=['reports_to']),
        ]

    def __str__(self):
        return f"{self.id} - {self.name}"


class Alert(models.Model):
    """
    Alert associated with an employee.
    """

    SEVERITY_LOW = 'low'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_HIGH = 'high'

    STATUS_OPEN = 'open'
    STATUS_DISMISSED = 'dismissed'

    SEVERITY_CHOICES = [
        (SEVERITY_LOW, 'Low'),
        (SEVERITY_MEDIUM, 'Medium'),
        (SEVERITY_HIGH, 'High'),
    ]

    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_DISMISSED, 'Dismissed'),
    ]

    id = models.CharField(max_length=16, primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='alerts')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_OPEN)

    class Meta:
        ordering = ['-created_at', 'id']
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def dismiss(self):
        """
        Idempotent dismiss operation.
        """
        if self.status != self.STATUS_DISMISSED:
            self.status = self.STATUS_DISMISSED
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Alert {self.id} ({self.severity})"
