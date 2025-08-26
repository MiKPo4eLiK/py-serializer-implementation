import json
from car.models import Car
from car.serializers import CarSerializer


def serialize_car_object(car_object: Car) -> str:
    serializer = CarSerializer(car_object)
    return json.dumps(serializer.data, indent=4)


def deserialize_car_object(json_data: str) -> Car:
    car_data = json.loads(json_data)
    serializer = CarSerializer(data=car_data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
python manage.py makemigrations