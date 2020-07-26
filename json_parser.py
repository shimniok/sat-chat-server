from flask.json import JSONEncoder
from datetime import datetime, timezone

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                #new = obj.replace(tzinfo=timezone.utc)
                #return new.isoformat()
                return datetime.strftime(obj, "%Y-%m-%dT%H:%M:%SZ")
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
