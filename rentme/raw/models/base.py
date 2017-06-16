from django.db import models


class RawModel():

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:

        pass
