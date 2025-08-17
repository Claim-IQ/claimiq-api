# complaints/serializers/logentry_serializers.py

from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from rest_framework import serializers


class LogEntrySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()
    log_message = serializers.SerializerMethodField()  # New field

    class Meta:
        model = LogEntry
        fields = ['user', 'action', 'object_repr',
                  'content_type', 'action_time', 'log_message']

    def get_user(self, obj):
        return obj.user.email if obj.user else "System / Deleted user"

    def get_action(self, obj):
        return {
            ADDITION: 'Added',
            CHANGE: 'Changed',
            DELETION: 'Deleted'
        }.get(obj.action_flag, 'Unknown')

    def get_content_type(self, obj):
        if obj.content_type:
            model_cls = obj.content_type.model_class()
            if model_cls:
                return getattr(model_cls._meta, 'verbose_name', model_cls.__name__).title()
        return "Unknown"

    def get_log_message(self, obj):
        """
        Construct a human-readable log message.
        Example: "owen@gmail.com added Producer Adidas at 2025-08-17T21:16:31.762373Z"
        """
        user = self.get_user(obj)
        action = self.get_action(obj).lower()
        content_type = self.get_content_type(obj)
        object_repr = obj.object_repr
        action_time = obj.action_time.strftime('%Y-%m-%d %H:%M:%S')
        return f'{user} {action} {content_type} "{object_repr}" at {action_time}'
