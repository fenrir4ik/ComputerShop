from rest_framework import serializers


class RepositorySerializer(serializers.Serializer):
    index = serializers.IntegerField(required=True)
    endpoint_name = serializers.CharField(required=True)
    endpoint_url = serializers.CharField(required=True)
    package_name = serializers.CharField(required=True)
    method_name = serializers.CharField(required=True)
    in_params = serializers.JSONField(required=True)
    out_params = serializers.JSONField(required=True)
    available = serializers.BooleanField(required=True)
