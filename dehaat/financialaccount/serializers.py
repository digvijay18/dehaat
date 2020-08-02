from rest_framework import serializers

from . import models


class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ledger
        fields = '__all__'

    def validate_amount(self, value):
        # On API request, negative values are not allowed. Positive values mean cash paid by customer
        # and ledger is updated.
        if value <= 0:
            raise serializers.ValidationError('Amount should be greater than 0.')
        return value
