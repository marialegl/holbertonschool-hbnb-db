#!/usr/bin/python3
"""Unittest for State"""

import unittest
from datetime import datetime
from state import State

class TestState(unittest.TestCase):

    def setUp(self):
        """Setup a default State instance for testing."""
        self.state = State(
            name="Test State",
            country="Test Country"
        )

    def test_state_creation(self):
        """Test that a State instance is created correctly."""
        self.assertEqual(self.state.name, "Test State")
        self.assertEqual(self.state.country, "Test Country")
        self.assertIsNotNone(self.state.id)
        self.assertIsInstance(self.state.created_at, datetime)
        self.assertIsInstance(self.state.updated_at, datetime)

    def test_add_city(self):
        """Test adding cities to a state."""
        self.state.add_city("Test City")
        self.assertIn("Test City", self.state.cities)

    def test_remove_city(self):
        """Test removing cities from a state."""
        self.state.add_city("Test City")
        self.state.remove_city("Test City")
        self.assertNotIn("Test City", self.state.cities)

    def test_update_attributes(self):
        """Test updating the attributes of a state."""
        self.state.update(name="Updated State", country="Updated Country")
        self.assertEqual(self.state.name, "Updated State")
        self.assertEqual(self.state.country, "Updated Country")

    def test_update_timestamp(self):
        """Test that the updated_at timestamp is updated on attribute update."""
        previous_updated_at = self.state.updated_at
        self.state.update(name="Another Update")
        self.assertNotEqual(self.state.updated_at, previous_updated_at)

    def test_state_str(self):
        """Test the string representation of the state."""
        self.assertEqual(str(self.state), f"State({self.state.id}, Test State, Test Country)")
 
    def test_state_delete(self):
        """Test that a state can be deleted."""
        state = State(name="Test State", country="Test Country")
        state_id = state.id
        state.delete()
        with self.assertRaises(NameError):
            print(state)

    def test_empty_name(self):
        """Test that an empty name raises a ValueError."""
        with self.assertRaises(ValueError):
            State(name="", country="Test Country")

    def test_empty_country(self):
        """Test that an empty country raises a ValueError."""
        with self.assertRaises(ValueError):
            State(name="Test State", country="")

if __name__ == "__main__":
    unittest.main()
