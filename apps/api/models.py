from django.db import models


class ApiPackage(models.Model):
    class Meta:
        db_table = 'api_package'

    package_name = models.CharField(max_length=100, unique=True)


class HttpMethod(models.Model):
    class Meta:
        db_table = 'http_method'

    method_name = models.CharField(max_length=10, unique=True)


class Endpoint(models.Model):
    class Meta:
        db_table = 'endpoint'

    endpoint_name = models.CharField(max_length=100, db_index=True)
    endpoint_url = models.CharField(max_length=255, db_index=True, unique=True)
    package = models.ForeignKey(ApiPackage, on_delete=models.CASCADE)
    methods = models.ManyToManyField(HttpMethod, related_name='endpoints', through='EndpointMethod')
    date_updated = models.DateTimeField(auto_now_add=True, blank=True)


class EndpointMethod(models.Model):
    class Meta:
        db_table = 'endpoint_has_method'

    in_params = models.JSONField()
    out_params = models.JSONField()
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    method = models.ForeignKey(HttpMethod, on_delete=models.CASCADE)
