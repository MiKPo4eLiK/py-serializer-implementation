import json
from car.models import Car
from car.serializers import CarSerializer

def serialize_car_object(car: Car) -> bytes:
    """Серіалізує об'єкт Car у JSON у байтах без пробілів"""
    from car.serializers import CarSerializer
    import json
    serializer = CarSerializer(car)
    return json.dumps(serializer.data, separators=(',', ':')).encode("utf-8")

def deserialize_car_object(json_data: str) -> Car:
    car_data = json.loads(json_data)
    serializer = CarSerializer(data=car_data)
    serializer.is_valid(raise_exception=True)
    return Car.objects.create(**serializer.validated_data)
