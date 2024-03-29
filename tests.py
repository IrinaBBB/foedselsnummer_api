import unittest
import functions


class TestsFnr(unittest.TestCase):
    def test_male_gender(self):
        # Test with a male gender
        fnr = "13123408766"
        expected_result = {"gender": "male"}
        self.assertEqual(functions.define_gender_json(fnr), expected_result)

    def test_female_gender(self):
        # Test with a female gender
        fnr = "27020974449"
        expected_result = {"gender": "female"}
        self.assertEqual(functions.define_gender_json(fnr), expected_result)

    def test_valid_age_63(self):
        # Test for 63 years old per today (13/03/2024)
        fnr = "13026110615"
        expected_result = {"age": 63}
        self.assertEqual(functions.calculate_age(fnr), expected_result)

    def test_valid_age_31(self):
        # Test for 31 years old per today (13/03/2024)
        fnr = "13059210615"
        expected_result = {"age": 31}
        self.assertEqual(functions.get_age_json(fnr), expected_result)

    def test_valid_age_24(self):
        # Test for 24 years old per today (13/03/2024)
        fnr = "080300923861"
        expected_result = {"age": 24}
        self.assertEqual(functions.get_age_json(fnr), expected_result)

    def test_invalid_format_age(self):
        # Test for 31 years old per today (13/03/2024)
        fnr = "81059210615"
        expected_result = {"error": "Incorrect formatting"}
        self.assertEqual(functions.calculate_age(fnr), expected_result)

    def test_fnr_validation_valid(self):
        fnr = "311299 46752"
        expected_result = True
        self.assertEqual(functions.validate_fnr(fnr), expected_result)

    def test_fnr_validation_invalid(self):
        fnr = "01042962793"
        expected_result = False
        self.assertEqual(functions.validate_fnr(fnr), expected_result)

    def test_fnr_is_not_numeric(self):
        fnr = "Anna Larsen"
        expected_result = False
        self.assertEqual(functions.validate_fnr(fnr), expected_result)


if __name__ == '__main__':
    unittest.main()
