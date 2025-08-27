# Import necessary modules
import json
from django.test import TestCase
from car.models import Car
from main import deserialize_car_object
from rest_framework.test import APITestCase
from car.serializers import CarSerializer


class TestSerializer(APITestCase):

    def setUp(self) -> None:
        """
        Set up the test data for each test.
        The data now matches the fields from the Car model and the serializer.
        """
        self.payload = {
            'manufacturer': 'Toyota',
            'model': 'Camry',
            'horse_powers': 203,
            'is_broken': True,
            'problem_description': 'Engine noise',
        }
        self.serializer = CarSerializer(data=self.payload)

    def test_contains_expected_fields(self) -> None:
        """
        Test that the serializer contains the correct expected fields.
        The list of expected fields is now aligned with the Car model and serializer.
        """
        serializer = CarSerializer()
        fields = serializer.fields.keys()
        expected_fields = [
            'id', 'manufacturer', 'model', 'horse_powers', 'is_broken', 'problem_description'
        ]
        self.assertEqual(set(fields), set(expected_fields))

    def test_fields_max_length(self) -> None:
        """
        Test that the fields have the correct max length.
        The test now checks for max_length=64 as defined in the model.
        """
        self.assertTrue(self.serializer.is_valid())
        self.assertEqual(self.serializer.fields['manufacturer'].max_length, 64)
        self.assertEqual(self.serializer.fields['model'].max_length, 64)

    def test_horse_powers_validators(self) -> None:
        """
        Test that the horse_powers field has the correct validators and range.
        The validators are defined in the serializer, overriding the model.
        """
        # Test a value that is within the valid range
        self.assertTrue(self.serializer.is_valid())

        # Test a value that is below the minimum allowed value
        payload_too_low = self.payload.copy()
        payload_too_low['horse_powers'] = 49
        serializer_low = CarSerializer(data=payload_too_low)
        self.assertFalse(serializer_low.is_valid())
        self.assertIn('horse_powers', serializer_low.errors)

        # Test a value that is above the maximum allowed value
        payload_too_high = self.payload.copy()
        payload_too_high['horse_powers'] = 1001
        serializer_high = CarSerializer(data=payload_too_high)
        self.assertFalse(serializer_high.is_valid())
        self.assertIn('horse_powers', serializer_high.errors)

    def test_problem_description_is_optional(self) -> None:
        """
        Test that the problem_description field is not required.
        """
        payload_without_problem = self.payload.copy()
        del payload_without_problem['problem_description']
        serializer = CarSerializer(data=payload_without_problem)
        self.assertTrue(serializer.is_valid())


class TestSerializerFunctions(TestCase):

    def setUp(self) -> None:
        """
        Set up test data for serializer functions.
        Note the use of the correct field names.
        """
        self.payload = {
            'manufacturer': 'Toyota',
            'model': 'Camry',
            'horse_powers': 203,
            'is_broken': True,
            'problem_description': 'Engine noise',
        }

    def test_deserialize_car(self) -> None:
        """
        Test that a car object is correctly deserialized from JSON.
        We now use `json.dumps` to convert the dictionary to a string,
        which is what the `deserialize_car_object` function expects.
        """
        # Convert the dictionary payload to a JSON string
        json_payload = json.dumps(self.payload)

        # Call the function with the JSON string
        car = deserialize_car_object(json_payload)

        # We expect a new Car instance with an ID assigned by the database
        self.assertIsInstance(car, Car)
        self.assertIsNotNone(car.id)

        # Now, check that the other fields match the payload
        self.assertEqual(car.manufacturer, self.payload['manufacturer'])
        self.assertEqual(car.model, self.payload['model'])
        self.assertEqual(car.horse_powers, self.payload['horse_powers'])
        self.assertEqual(car.is_broken, self.payload['is_broken'])
        self.assertEqual(car.problem_description, self.payload['problem_description'])
