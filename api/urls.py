from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CompanyViewSet, ComplaintViewSet, LogEntryViewSet,
                    ProducerViewSet, StatisticsViewSet, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'producers', ProducerViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'logs', LogEntryViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
