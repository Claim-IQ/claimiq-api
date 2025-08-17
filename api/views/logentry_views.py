# complaints/views/logentry_views.py

from django.contrib.admin.models import LogEntry
from rest_framework import permissions, viewsets

from ..serializers.logentry_serializers import LogEntrySerializer


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that returns recent admin actions.
    """
    queryset = LogEntry.objects.select_related(
        'user', 'content_type').order_by('-action_time')[:50]
    serializer_class = LogEntrySerializer
    # or IsAdminUser if you want
    permission_classes = [permissions.IsAuthenticated]
