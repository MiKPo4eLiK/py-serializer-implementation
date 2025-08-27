from django.test import TestCase
from car.models import Car
from main import deserialize_car_object
from rest_framework.test import APITestCase
from car.serializers import CarSerializer


class TestSerializer(APITestCase):

    def setUp(self) -> None:
        """
        Set up the test data for each test.
        We'll create a dictionary with car data.
        """
        self.payload = {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'horsepower': 203,
            'problem_description': 'Engine noise',
        }

    def test_contains_expected_fields(self) -> None:
        """Test that the serializer contains the expected fields."""
        serializer = CarSerializer()
        fields = serializer.fields.keys()
        expected_fields = ['make', 'model', 'year', 'horsepower', 'problem_description']
        self.assertEqual(set(fields), set(expected_fields))

    def test_fields_max_length(self) -> None:
        """Test that the fields have the correct max length."""
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.fields['make'].max_length, 100)
        self.assertEqual(serializer.fields['model'].max_length, 100)

    def test_horsepower(self) -> None:
        """Test that horsepower is a positive integer."""
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data['horsepower'] > 0)

    def test_year(self) -> None:
        """Test that year is a valid year."""
        serializer = CarSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data['year'] > 1900)

    def test_problem_description_is_not_required(self) -> None:
        """Test that the problem description field is not required."""
        payload_without_problem = self.payload.copy()
        payload_without_problem.pop('problem_description')
        serializer = CarSerializer(data=payload_without_problem)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('problem_description', serializer.validated_data)


class TestSerializerFunctions(TestCase):

    def setUp(self) -> None:
        """
        Set up test data for serializer functions.
        Note: We are not hard-coding the 'id' field anymore.
        """
        self.payload = {
            'make': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'horsepower': 203,
            'problem_description': 'Engine noise',
        }

    def test_deserialize_car(self) -> None:
        """
        Test that a car object is correctly deserialized from JSON.
        We check for the existence of an ID and then compare the other fields.
        """
        # Call the function that creates the car object from JSON
        car = deserialize_car_object(self.payload)

        # We expect a new Car instance with an ID assigned by the database
        self.assertIsInstance(car, Car)
        self.assertIsNotNone(car.id)

        # Now, check that the other fields match the payload
        self.assertEqual(car.make, self.payload['make'])
        self.assertEqual(car.model, self.payload['model'])
        self.assertEqual(car.year, self.payload['year'])
        self.assertEqual(car.horsepower, self.payload['horsepower'])
        self.assertEqual(car.problem_description, self.payload['problem_description'])
