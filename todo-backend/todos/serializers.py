from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoEngine uses 'id' as string
    name = serializers.CharField(max_length=200, required=True)
    price = serializers.FloatField(required=True)
    quantity = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Stock(**validated_data).save()

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


