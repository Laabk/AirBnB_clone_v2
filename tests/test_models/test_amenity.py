#!/usr/bin/python3
"""he amenity test"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
import pep8
import os

class TestAmenity(unittest.TestCase):
    """ test for the Amenity class"""

    @classmethod
    def setUpClass(cls):
        """the test setup"""
        cls.amenity = Amenity()
        cls.amenity.name = "Breakfast"

    @classmethod
    def teardown(cls):
        """tear it down test at the end of it use"""
        del cls.amenity

    def tearDown(self):
        """the teardown method"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Amenity(self):
        """ pep8 style test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/amenity.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_Amenity(self):
        """docstrings presences"""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes_Amenity(self):
        """test for amenity have attibutes"""
        self.assertTrue('id' in self.amenity.__dict__)
        self.assertTrue('created_at' in self.amenity.__dict__)
        self.assertTrue('updated_at' in self.amenity.__dict__)
        self.assertTrue('name' in self.amenity.__dict__)

    def test_is_subclass_Amenity(self):
        """test Amenity subclass of Basemodel"""
        self.assertTrue(issubclass(self.amenity.__class__, BaseModel), True)

    def test_attribute_types_Amenity(self):
        """test Amenity"""
        self.assertEqual(type(self.amenity.name), str)

    def test_save_Amenity(self):
        """test to ensure the save works"""
        self.amenity.save()
        self.assertNotEqual(self.amenity.created_at, self.amenity.updated_at)

    def test_to_dict_Amenity(self):
        """test for dictionary"""
        self.assertEqual('to_dict' in dir(self.amenity), True)


if __name__ == "__main__":
    unittest.main()
