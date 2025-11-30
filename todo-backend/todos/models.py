from mongoengine import Document, StringField, FloatField, IntField, DateTimeField


class Stock(Document):
    name = StringField(required=True, max_length=200)
    price = FloatField(required=True)
    quantity = IntField(required=True)

