from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator

MIN_HP = 50
MAX_HP = 1000


class CarSerializer(serializers.Serializer):
    manufacturer = serializers.CharField(max_length=64)
    model = serializers.CharField(max_length=64)
    horse_powers = serializers.IntegerField(
        validators=[
            MinValueValidator(MIN_HP),
            MaxValueValidator(MAX_HP)
        ]
    )
    is_broken = serializers.BooleanField()
    problem_description = serializers.CharField(
        required=False, allow_null=True)

    def create(self, validated_data) -> dict:
        return validated_data

    def update(self, instance, validated_data) -> dict:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
