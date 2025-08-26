from django.test import TransactionTestCase

from car.models import Car
from main import serialize_car_object, deserialize_car_object
from car.serializers import CarSerializer


class TestSerializer(TransactionTestCase):

    def setUp(self) -> None:
        self.payload = {
            "id": 1,
            "manufacturer": "Audi",
            "model": "A4",
            "horse_powers": 200,
            "is_broken": True,
            "problem_description": "test description",
        }

        self.serializer_data = {
            "manufacturer": "Mercedes",
            "model": "CLS",
            "horse_powers": 300,
            "is_broken": False,
            "problem_description": "test description",
        }

        self.car = Car.objects.create(**self.payload)
        self.serializer = CarSerializer(instance=self.car)

    def test_contains_expected_fields(self):
        self.assertEqual(
            self.serializer.data.keys(),
            {
                "id",
                "manufacturer",
                "model",
                "horse_powers",
                "is_broken",
                "problem_description",
            },
        )

    def test_serializer_fields(self):
        for key in self.serializer.data:
            with self.subTest(key):
                self.assertEqual(self.serializer.data[key], self.payload[key])

    def test_horse_powers(self):
        items = [0, 2000]

        for item in items:
            with self.subTest(f"horse_powers={item}"):
                self.serializer_data["horse_powers"] = item
                serializer = CarSerializer(data=self.serializer_data)

                self.assertFalse(serializer.is_valid())

    def test_fields_max_length(self):
        items = [
            ("manufacturer", "Extremely long test manufacturer Extremely long test manufacturer"),
            ("model", "Extremely long test model Extremely long test model Extremely long test model")
        ]

        for item in items:
            with self.subTest(f"{item[0]} max_length"):
                self.serializer_data[item[0]] = item[1]
                serializer = CarSerializer(data=self.serializer_data)

                self.assertFalse(serializer.is_valid())

    def test_problem_description_is_not_required(self):
        self.serializer_data.pop("problem_description")

        serializer = CarSerializer(data=self.serializer_data)

        self.assertTrue(serializer.is_valid())


class TestSerializerFunctions(TransactionTestCase):

    def setUp(self) -> None:
        self.payload = {
            "id": 1,
            "manufacturer": "Audi",
            "model": "A4",
            "horse_powers": 200,
            "is_broken": True,
            "problem_description": "test description",
        }

    def test_serialize_car(self):
        car = Car(**self.payload)
        result = '{"id":1,"manufacturer":"Audi","model":"A4","horse_powers":200,' \
                 '"is_broken":true,"problem_description":"test description"}'

        self.assertEqual(serialize_car_object(car=car), bytes(result, "utf-8"))

    def test_deserialize_car(self):
        json = b'{"id":1,"manufacturer":"Audi","model":"A4",' \
                    b'"horse_powers":200,"is_broken":true,"problem_description":"test description"}'

        car = deserialize_car_object(json)

        for field in self.payload:
            with self.subTest(field):
                self.assertEqual(getattr(car, field), self.payload[field])
        self.assertIsInstance(car, Car)
