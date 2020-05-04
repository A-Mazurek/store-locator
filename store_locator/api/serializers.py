from marshmallow import Schema, fields


class CitesList(Schema):
    name = fields.Str()
    postcode = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()


class CitesInRangeList(CitesList):
    distance = fields.Str()
