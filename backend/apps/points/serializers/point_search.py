from rest_framework import serializers

from apps.points.models import Point


class PPEFilterSerializer(serializers.Serializer):
    ppe_number = serializers.CharField(required=False)
    nip = serializers.CharField(required=False)
    receiver = serializers.CharField(required=False)
    seller = serializers.CharField(required=False)
    tariff = serializers.CharField(required=False)
    counter_number = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    osd_number = serializers.CharField(required=False)
    sort_by = serializers.ChoiceField(
        choices=["annual_consumption", "created_at", "receiver"],
        required=False
    )


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = [
            "id", "name", "city", "street", "street_number",
            "zip_code", "post", "ppe_number", "osd_number",
            "counter_number", "tariff", "power", "osd_next",
            "seller_change", "seller", "contract_type",
            "notice_period", "contract_duration", "termination_date",
            "sale_start", "sale_end", "verified", "created_at",
            "modified_at", "annual_consumption", "division"
        ]