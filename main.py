import json
from car.serializers import CarSerializer


class Car:
    def __init__(self, manufacturer, model, horse_powers,
                 is_broken, problem_description=None) -> None:
        self.manufacturer = manufacturer
        self.model = model
        self.horse_powers = horse_powers
        self.is_broken = is_broken
        self.problem_description = problem_description


def serialize_car_object(car_object) -> str:
    serializer = CarSerializer(car_object)
    return json.dumps(serializer.data, indent=4)


def deserialize_car_object(json_data) -> object:
    car_data = json.loads(json_data)
    serializer = CarSerializer(data=car_data)
    if serializer.is_valid():
        car_instance = serializer.create(serializer.validated_data)
        return Car(**car_instance)
    else:
        print("Validation errors:", serializer.errors)
        return None
