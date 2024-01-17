#!/usr/bin/python3
"""test for the BaseModel"""
import unittest
from models.base_model import BaseModel
import pep8
import os
from models.engine.file_storage import FileStorage
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """test for the base model class"""

    @classmethod
    def setUpClass(cls):
        """the test setup"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base = BaseModel()

    @classmethod
    def teardown(cls):
        """tear it down test at the end of process"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.storage

    def test_pep8_BaseModel(self):
        """pep8 test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/base_model.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_BaseModel(self):
        """docstrings in basemodel"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)
        self.assertIsNotNone(BaseModel.delete.__doc__)

    def test_method_BaseModel(self):
        """Basemodel methods"""
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))
        self.assertTrue(hasattr(BaseModel, "__str__"))
        self.assertTrue(hasattr(BaseModel, "delete"))

    def test_init_BaseModel(self):
        """testto ensre base is an type BaseModel"""
        self.assertTrue(isinstance(self.base, BaseModel))

    def test_kwargs(self):
        """Test initialization of the args and kwargs."""
        date = datetime.utcnow()
        BModel = BaseModel("1", id="3", created_at=date.isoformat())
        self.assertEqual(BModel.id, "3")
        self.assertEqual(BModel.created_at, date)

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Test DBS")
    def test_save_BaesModel(self):
        """test to ensure save works"""
        prev = self.base.updated_at
        self.base.save()
        self.assertLess(prev, self.base.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("BaseModel.{}".format(self.base.id), f.read())
        self.assertNotEqual(self.base.created_at, self.base.updated_at)

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Test DBS")
    def test_delete(self):
        self.base.delete()
        self.assertNotIn(self.base, FileStorage._FileStorage__objects)

    def test_to_dict_BaseModel(self):
        """test to ensure dictionary works"""
        base_dict = self.base.to_dict()
        self.assertEqual(self.base.__class__.__name__, 'BaseModel')
        self.assertIsInstance(base_dict['created_at'], str)
        self.assertIsInstance(base_dict['updated_at'], str)


if __name__ == "__main__":
    unittest.main()
