from rest_framework import serializers

from ..models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    type = serializers.StringRelatedField()
    status = serializers.StringRelatedField()
    decision = serializers.StringRelatedField()
    registration_unit = serializers.StringRelatedField()

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['submit_date', 'deadline']
