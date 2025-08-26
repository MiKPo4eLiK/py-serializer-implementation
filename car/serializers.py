from rest_framework import serializers
from .models import Car
from django.core.validators import MinValueValidator, MaxValueValidator

MIN_HP = 50
MAX_HP = 1000


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
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
        required=False, allow_null=True, allow_blank=True
    )

    def create(self, validated_data) -> Car:
        return Car.objects.create(**validated_data)

    def update(self, instance: Car, validated_data) -> Car:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
