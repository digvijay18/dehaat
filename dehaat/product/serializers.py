from . import models
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # TODO: Replace __all__ with explicit field names.
        model = models.Product
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.features)
        instance.features = validated_data.get('features', instance.features)
        instance.price = validated_data.get('price', instance.price)
        instance.units = validated_data.get('units', instance.units)
        instance.active = validated_data.get('active', instance.active)
        instance.save(update_fields=['description', 'features', 'price', 'units', 'active'])
        return instance
