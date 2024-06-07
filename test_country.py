import unittest
from country import Country


class TestCountry(unittest.TestCase):

    def test_initialization(self):
        country = Country(id="1234", name="Testland")
        self.assertEqual(country.id, "1234")
        self.assertEqual(country.name, "Testland")
        self.assertEqual(country.cities, [])

    def test_add_city(self):
        country = Country(id="1234", name="Testland")
        country.addCity("CityA")
        self.assertIn("CityA", country.cities)

    def test_remove_city(self):
        country = Country(id="1234", name="Testland", cities=["CityA", "CityB"])
        country.removeCity("CityA")
        self.assertNotIn("CityA", country.cities)
        country.removeCity("CityC")

    def test_update_name(self):
        country = Country(id="1234", name="Testland")
        country.update("Newland")
        self.assertEqual(country.name, "Newland")

    def test_str_representation(self):
        country = Country(id="1234", name="Testland", cities=["CityA", "CityB"])
        expected_str = "Country(ID: 1234, Name: Testland, Cities: [CityA, CityB])"
        self.assertEqual(str(country), expected_str)

if __name__ == '__main__':
    unittest.main()
