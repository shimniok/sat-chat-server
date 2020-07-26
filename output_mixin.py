# Provides SqlAlchemy model serialization to json
# https://mmas.github.io/sqlalchemy-serialize-json

from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import datetime
from flask.json import JSONEncoder


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False
    PROTECTED_COLUMNS = []

    def __iter__(self):
        return self.to_dict().iteritems()

    # return only list of columns not in PROTECTED_COLUMNS
    def get_unprotected_items(self):
        list = []
        for i in self.__mapper__.c.items():
            attr, column = i
            if not column.key in self.PROTECTED_COLUMNS:
                list.append(i)
        return list

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr) for attr, column in self.get_unprotected_items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between two tables.
                #TODO: Fix recursion problem with bidirectional relations
                if hasattr(relation, 'table') and backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)
