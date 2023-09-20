import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestConsole(unittest.TestCase):
    """Test cases for the console"""

    def setUp(self):
        """Set up for the test"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Tear down for the test"""
        pass

    def test_do_create(self):
        """Test do_create method"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("MyModel")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test'")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number=1")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number=1.5")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1'")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1.5'")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1.5' string='hello world'")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1.5' string='hello world' bool=True")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1.5' string='hello world' bool=True list=[1, 2, 3]")
            self.assertTrue(len(f.getvalue().strip()) == 36)

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.do_create("BaseModel name='test' number='1.5' string='hello world' bool=True list=[1, 2, 3] dict={'key': 'value'}")
            self.assertTrue(len(f.getvalue().strip()) == 36)