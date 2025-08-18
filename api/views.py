# Import all viewsets from the new package structure
from .views import (CompanyViewSet, ComplaintViewSet, ProducerViewSet,
                    StatisticsViewSet, UserViewSet)

__all__ = [
    'UserViewSet',
    'CompanyViewSet',
    'ProducerViewSet',
    'ComplaintViewSet',
    'StatisticsViewSet'
]
