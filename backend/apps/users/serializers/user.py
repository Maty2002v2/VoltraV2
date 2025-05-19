from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
import json

from apps.points.models.point_cost import PointCost
from apps.division.models.division import Division
from apps.points.models.point import Point
from apps.users.models.change_history import ChangeHistory

class ContactDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    client_number = serializers.CharField(required=False)

    def update(self, instance, validated_data):
        """ Aktualizacja użytkownika oraz powiązanego profilu """
        changed_fields = {}

        # 🔹 Aktualizacja pól w modelu User
        for field in ['first_name', 'last_name', 'email']:
            if field in validated_data:
                old_value = getattr(instance, field, None)
                new_value = validated_data[field]
                if old_value != new_value:
                    changed_fields[field] = {"old": old_value, "new": new_value}
                    setattr(instance, field, new_value)

        # 🔹 Aktualizacja pól w modelu UserProfile
        profile = instance.profile  # Pobieramy profil użytkownika
        for field in ['phone_number', 'client_number']:
            if field in validated_data:
                old_value = getattr(profile, field, None)
                new_value = validated_data[field]
                if old_value != new_value:
                    changed_fields[field] = {"old": old_value, "new": new_value}
                    setattr(profile, field, new_value)

        instance.save()
        profile.save()

        for field, values in changed_fields.items():
            ChangeHistory.objects.create(
                user_id=instance.id,
                field_name=field,
                old_value=str(values['old']),
                new_value=str(values['new']),
            )

        return instance

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ["id", "name", "receiver", "nip", "address", "company_address"]

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = [
            "id", "name", "city", "street", "street_number", "zip_code", "post",
            "ppe_number", "osd_number", "counter_number", "tariff", "power",
            "osd_next", "seller_change", "seller", "contract_type", "notice_period",
            "contract_duration", "termination_date", "sale_start", "sale_end",
            "verified", "annual_consumption", "division"
        ]
