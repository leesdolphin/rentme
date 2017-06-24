import datetime
import json

from django.db import models


class JSONEncoder(json  .JSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, RawModel):
            dikt = {}
            for attr, stype in o.swagger_types.items():
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                elif stype.startswith('list['):
                    value = list(value.all())
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)


class RawModel(models.Model):

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

    def __repr__(self):
        return json.dumps(self, indent=2, cls=JSONEncoder)
