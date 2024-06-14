#!/usr/bin/python3
"""Unittest for Country"""

import unittest
from model.country import Country


class TestCountry(unittest.TestCase):

    def test_initialization(self):
        country = Country(id="1234", name="Testland")
        self.assertEqual(country.id, "1234")
        self.assertEqual(country.name, "Testland")
        self.assertEqual(country.states, [])

    def test_add_state(self):
        country = Country(id="1234", name="Testland")
        country.add_state("StateA")
        self.assertIn("StateA", country.states)

    def test_remove_state(self):
        country = Country(id="1234", name="Testland", states=["StateA", "StateB"])
        country.remove_state("StateA")
        self.assertNotIn("StateA", country.states)
        country.remove_state("StateC")

    def test_update_name(self):
        country = Country(id="1234", name="Testland")
        country.update("Newland")
        self.assertEqual(country.name, "Newland")

    def test_str_representation(self):
        country = Country(id="1234", name="Testland", states=["StateA", "StateB"])
        expected_str = "Country(ID: 1234, Name: Testland, States: [StateA, StateB])"
        self.assertEqual(str(country), expected_str)

if __name__ == '__main__':
    unittest.main()