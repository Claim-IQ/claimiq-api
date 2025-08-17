from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ActionHistoryViewSet, CompanyViewSet, ComplaintViewSet,
                    ProducerViewSet, StatisticsViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'producers', ProducerViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'action-history', ActionHistoryViewSet)
router.register(r'statistics', StatisticsViewSet, basename='statistics')

urlpatterns = [
    path('', include(router.urls)),
]
