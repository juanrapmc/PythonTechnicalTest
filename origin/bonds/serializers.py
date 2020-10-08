from rest_framework import serializers
from bonds.models import Bond


class BondSerializer(serializers.ModelSerializer):
    legal_name = serializers.ReadOnlyField()

    class Meta:
        model = Bond
        fields = ["isin", "size", "currency", "maturity", "lei", "legal_name"]
