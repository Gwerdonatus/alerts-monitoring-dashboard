from typing import List, Set

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        scope = request.query_params.get("scope", "direct")
        if scope not in VALID_SCOPES:
            return Response(
                {"detail": "Invalid scope"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        manager = self._manager_for(request)

        employee_ids: List[str] = (
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

    @staticmethod
    def _manager_for(request: Request) -> Employee:
        try:
            return request.user.employee_profile
        except Employee.DoesNotExist as exc:
            raise PermissionDenied("Authenticated user has no employee profile") from exc

    def _apply_filters(self, request: Request, queryset):
        """Apply severity, status, and search filters to the queryset."""
        severity = request.query_params.get("severity")
        if severity:
            severities = severity.split(",")
            self._validate_values(severities, VALID_SEVERITIES, "severity")
            queryset = queryset.filter(severity__in=severities)

        status_param = request.query_params.get("status")
        if status_param:
            statuses = status_param.split(",")
            self._validate_values(statuses, VALID_STATUSES, "status")
            queryset = queryset.filter(status__in=statuses)

        search = request.query_params.get("q")
        if search:
            queryset = queryset.filter(employee__name__icontains=search)

        return queryset

    @staticmethod
    def _validate_values(values: List[str], allowed: Set[str], field_name: str) -> None:
        """Validate that all values are in the allowed set."""
        invalid = sorted(set(values) - allowed)
        if invalid:
            raise ValidationError(
                {field_name: [f"Unsupported value: {value}" for value in invalid]}
            )


class DismissAlertAPIView(APIView):
    """
    Dismiss an alert (idempotent).
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk: str) -> Response:
        manager = AlertsListAPIView._manager_for(request)
        alert = get_object_or_404(
            Alert.objects.select_related("employee"),
            pk=pk,
            employee_id__in=get_subtree_report_ids(manager),
        )
        alert.dismiss()
        serializer = AlertSerializer(alert)
        return Response(serializer.data, status=status.HTTP_200_OK)
