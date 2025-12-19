from django.urls import path
from .views import AlertsListAPIView, DismissAlertAPIView

urlpatterns = [
    path('api/alerts', AlertsListAPIView.as_view(), name='list'),
    path('api/alerts/<str:pk>/dismiss', DismissAlertAPIView.as_view(), name='dismiss'),
]
