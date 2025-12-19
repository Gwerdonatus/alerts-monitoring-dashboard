from typing import List, Set

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import Employee, Alert
from .serializers import AlertSerializer
from .services import get_direct_report_ids, get_subtree_report_ids
from .pagination import StandardResultsSetPagination


VALID_SCOPES: Set[str] = {"direct", "subtree"}
VALID_SEVERITIES: Set[str] = {"low", "medium", "high"}
VALID_STATUSES: Set[str] = {"open", "dismissed"}


class AlertsListAPIView(APIView):
    """
    List alerts for a manager's direct or subtree reports.

    Supports filtering by:
    - scope: direct | subtree
    - severity: comma-separated values
    - status: comma-separated values
    - q: employee name search
    """

    pagination_class = StandardResultsSetPagination

    def get(self, request: Request) -> Response:
        manager_id = request.query_params.get("manager_id")
        if not manager_id:
            return Response(
                {"detail": "manager_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        scope = request.query_params.get("scope", "direct")
        if scope not in VALID_SCOPES:
            return Response(
                {"detail": "Invalid scope"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        manager = get_object_or_404(Employee, pk=manager_id)

        employee_ids: List[int] = (
            get_direct_report_ids(manager)
            if scope == "direct"
            else get_subtree_report_ids(manager)
        )

        queryset = (
            Alert.objects.filter(employee_id__in=employee_ids)
            .select_related("employee")
            .order_by("-created_at")
        )

        queryset = self._apply_filters(request, queryset)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = AlertSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def _apply_filters(self, request: Request, queryset):
        """Apply severity, status, and search filters to the queryset."""
        severity = request.query_params.get("severity")
        if severity:
            severities = severity.split(",")
            try:
                self._validate_values(severities, VALID_SEVERITIES, "severity")
            except ValueError:
                return queryset.none()
            queryset = queryset.filter(severity__in=severities)

        status_param = request.query_params.get("status")
        if status_param:
            statuses = status_param.split(",")
            try:
                self._validate_values(statuses, VALID_STATUSES, "status")
            except ValueError:
                return queryset.none()
            queryset = queryset.filter(status__in=statuses)

        search = request.query_params.get("q")
        if search:
            queryset = queryset.filter(employee__name__icontains=search)

        return queryset

    @staticmethod
    def _validate_values(values: List[str], allowed: Set[str], field_name: str) -> None:
        """Validate that all values are in the allowed set."""
        if any(value not in allowed for value in values):
            raise ValueError(f"Invalid {field_name}")


class DismissAlertAPIView(APIView):
    """
    Dismiss an alert (idempotent).
    """

    def post(self, request: Request, pk: str) -> Response:
        alert = get_object_or_404(Alert, pk=pk)
        alert.dismiss()
        serializer = AlertSerializer(alert)
        return Response(serializer.data, status=status.HTTP_200_OK)
