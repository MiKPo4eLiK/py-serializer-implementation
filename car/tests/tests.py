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
        The data now uses the correct field names: 'manufacturer' and 'horse_powers'.
        We also include 'is_broken' as indicated by the traceback.
        """
        self.payload = {
            'manufacturer': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'horse_powers': 203,
            'is_broken': True,
        }

    def test_contains_expected_fields(self) -> None:
        """
        Test that the serializer contains the correct expected fields.
        We now check for the fields found in the traceback:
        'id', 'manufacturer', 'model', 'year', 'horse_powers', 'is_broken'.
        """
        serializer = CarSerializer()
        fields = serializer.fields.keys()
        expected_fields = [
            'id', 'manufacturer', 'model', 'year', 'horse_powers', 'is_broken'
        ]
        self.assertEqual(set(fields), set(expected_fields))

    def test_fields_max_length(self) -> None:
        """
        Test that the fields have the correct max length.
        The test now uses the correct field name 'manufacturer'.
        """
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.fields['manufacturer'].max_length, 100)
        self.assertEqual(serializer.fields['model'].max_length, 100)

    def test_horse_powers(self) -> None:
        """
        Test that horse_powers is a positive integer.
        The test now uses the correct field name 'horse_powers'.
        """
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data['horse_powers'] > 0)

    def test_year(self) -> None:
        """Test that year is a valid year."""
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data['year'] > 1900)

    def test_is_broken(self) -> None:
        """Test that is_broken field is present and a boolean."""
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertIn('is_broken', serializer.validated_data)
        self.assertIsInstance(serializer.validated_data['is_broken'], bool)


class TestSerializerFunctions(TestCase):

    def setUp(self) -> None:
        """
        Set up test data for serializer functions.
        Note the use of the correct field names.
        """
        self.payload = {
            'manufacturer': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'horse_powers': 203,
            'is_broken': True,
        }

    def test_deserialize_car(self) -> None:
        """
        Test that a car object is correctly deserialized from JSON.
        We now use `json.dumps` to convert the dictionary to a string,
        which is what the `deserialize_car_object` function expects.
        """
        json_payload = json.dumps(self.payload)

        car = deserialize_car_object(json_payload)

        self.assertIsInstance(car, Car)
        self.assertIsNotNone(car.id)

        self.assertEqual(car.manufacturer, self.payload['manufacturer'])
        self.assertEqual(car.model, self.payload['model'])
        self.assertEqual(car.year, self.payload['year'])
        self.assertEqual(car.horse_powers, self.payload['horse_powers'])
        self.assertEqual(car.is_broken, self.payload['is_broken'])
