"""
Contains the tests for the console
"""
import unittest
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch

import sys
import os


def setUpModule():
    """Set up resources to be used in the test module"""
    if os.path.isfile("file.json"):
        os.rename("file.json", "tmp.json")


def tearDownModule():
    """Tear down resources used in the test module"""
    if os.path.isfile("file.json"):
        os.remove("file.json")
    if os.path.isfile("tmp.json"):
        os.rename("tmp.json", "file.json")


class TestHBNBCommand(unittest.TestCase):
    """Tests for the HBNBCommand prompt"""

    def test_HBNBCommand_prompt(self):
        """Test the HBNBCommand prompt"""
        self.assertEqual(HBNBCommand.prompt, '(hbnb) ')

    def test_empty_line(self):
        """Test output when an empty line is passed"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("")
            self.assertEqual("", f.getvalue().strip())


class TestHBNBCommand_create(unittest.TestCase):
    """Test the HBNBCommand create command"""

    def test_HBNBCommand_create_error_messages(self):
        """Test that the create comand prints the correct error messages"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_HBNBCommand_create_new_instances(self):
        """Test the creation of new instances of different classes"""

        Mm = ['BaseModel', 'User', 'Place',
              'City', 'State', 'Review', 'Amenity']
        for m in Mm:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('create {}'.format(m))
                new_key = m + "." + f.getvalue().strip()
                self.assertIn(new_key, storage.all().keys())


class TestHBNBCommand_create_with_parameters(unittest.TestCase):
    """Test the create command when parameters are passed"""

    def test_HBNBCommand_create_new_instances_with_pars(self):
        """Test creation of new instances with parameters"""
        Mm = ['BaseModel', 'User', 'Place',
              'City', 'State', 'Review', 'Amenity']

        for m in Mm:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('''create {}
                    city_id="0001" user_id="0001" name="My_little_house"
                    number_rooms=4 number_bathrooms=2 max_guest=10
                    price_by_night=300 latitude=37.773972 longitude=-122.431297
                                     '''.format(m))

                new_key = m + "." + f.getvalue().strip()
                self.assertIn(new_key, storage.all().keys())


class TestHBNBCommand_show(unittest.TestCase):
    """Test the HBNBCommand show command"""

    def test_HBNBCommand_show_error_messages(self):
        """Test that the show comand prints the correct error messages"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show')
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show BaseModel')
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show BaseModel 12234321')
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_HBNBCommand_show_existing_instance(self):
        """Test the creation of new instances of different classes"""
        objs = storage.all()
        for key, value in objs.items():
            inst = key.split(".")
            value_str = str(value)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('show {} {}'.format(inst[0], inst[1]))
                self.assertEqual(value_str, f.getvalue().strip())


class TestHBNBCommand_destroy(unittest.TestCase):
    """Test the HBNBCommand destroy command"""

    def test_HBNBCommand_destroy_error_messages(self):
        """Test that the destroy comand prints the correct error messages"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy')
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy BaseModel')
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy BaseModel 12234321')
            self.assertEqual("** no instance found **", f.getvalue().strip())

    def test_HBNBCommand_destroy_existing_instances(self):
        """Test the destruction of new instances of different classes"""

        Mm = ['BaseModel', 'User', 'Place',
              'City', 'State', 'Review', 'Amenity']
        my_objs = {}
        for m in Mm:
            tmp = eval(m)()
            tmp.save()
            tmp_id = m + "." + tmp.id
            my_objs[tmp_id] = tmp
        for key in my_objs.keys():
            kk = key.split(".")
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('destroy {} {}'.format(kk[0], kk[1]))
                objs = storage.all()
                self.assertNotIn(kk[1], objs.keys())


class TestHBNBCommand_all(unittest.TestCase):
    """Test the HBNBCommand all command"""

    def test_HBNBCommand_all_error_messages(self):
        """Test that the all comand prints the correct error messages"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_HBNBCommand_all_existing_instances(self):
        """Test the creation of new instances of different classes"""

        objs = storage.all()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('all')
            for key, value in objs.items():
                inst_key = key.split(".")[1]
                self.assertIn(inst_key, f.getvalue().strip())

    def test_HBNBCommand_all_existing_instances_specific_class(self):
        """Test the creation of new instances of different classes"""

        Mm = ['BaseModel', 'User', 'Place',
              'City', 'State', 'Review', 'Amenity']
        for m in Mm:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('all {}'.format(m))
                for n in Mm:
                    if n != m:
                        self.assertNotIn(n, f.getvalue().strip())


class TestHBNBCommand_update(unittest.TestCase):
    """Test the HBNBCommand update command"""

    def test_HBNBCommand_update_error_messages(self):
        """Test that the update comand prints the correct error messages"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update')
            self.assertEqual("** class name missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update MyModel')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel')
            self.assertEqual("** instance id missing **", f.getvalue().strip())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel 12234321')
            self.assertEqual("** no instance found **", f.getvalue().strip())

        objs = storage.all()
        for key, value in objs.items():
            kk = key.split(".")
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('update {} {}'.format(kk[0], kk[1]))
                self.assertEqual("** attribute name missing **",
                                 f.getvalue().strip())

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('update {} {} id'.format(kk[0], kk[1]))
                self.assertEqual("** value missing **",
                                 f.getvalue().strip())

    def test_HBNBCommand_update_existing_instance(self):
        """Test the creation of new instances of different classes"""
        objs = storage.all()
        key = list(objs.keys())[0].split(".")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update {} {} name Silvia'.format(key[0],
                                                                   key[1]))
            HBNBCommand().onecmd('show {} {}'.format(key[0], key[1]))
            self.assertIn('name', f.getvalue().strip())
            self.assertIn('Silvia', f.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
