from django.db import models


class RawModel(models.Model):

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True


print("LOADED")
