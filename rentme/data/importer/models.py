from django.db import models


class CachedResponse(models.Model):

    class Meta:
        unique_together = (
            ('method', 'url', 'kwargs')
        )

    method = models.CharField(max_length=10)
    url = models.TextField()
    kwargs = models.TextField()

    content = models.BinaryField()
    data = models.TextField()

    expiry = models.DateTimeField()
