try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    import cStringIO
except ImportError:
    import io as cStringIO
import os
import sys
sys.path.append("..")
from src.property import Property

class TestProperty(unittest.TestCase):
    """ Tests for module 'property'.
    """
    @classmethod
    def setUpClass(cls):
        cls.tempf = "temp.test_pro"
        cls.string = "1.0"
        cls.stdout = sys.stdout
        cls.stderr = sys.stderr
        #TODO stderr not right now although test_run passed.

        sys.stdout = cStringIO.StringIO()
        sys.stderr = cStringIO.StringIO()
        with open(cls.tempf, "wt") as f:
            f.write(cls.string)

    def test_init(self):
        _prop = Property(self.tempf)
        self.assertEqual(self.tempf, _prop.name)
        self.assertEqual(1, len([f for f in os.listdir('.')
                                 if f.startswith(self.tempf + '#')]))
        self.assertFalse(os.path.exists(self.tempf))

    def test_update_property_list(self):
        _prop = Property(self.tempf)
        _prop.value = "1.0"
        _prop.update_property_list()
        f = open(self.tempf, "rt")
        lines = f.readlines()
        self.assertEqual("1.0\n", lines[-1])

    def test_target_function(self):
        _prop = Property(self.tempf)
        _prop.value = 1.0
        _prop.reference = 1.0
        self.assertEqual(0.0, _prop.target_function())
        _prop.value = 2.0
        self.assertEqual(1.0, _prop.target_function())
        _prop.special = ["foo", "bar"]
        self.assertRaises(ValueError, _prop.target_function)
        _prop.special = ["scaled", "10"]
        self.assertEqual(10.0, _prop.target_function())
        _prop.special[0] = "log"
        self.assertRaises(ZeroDivisionError, _prop.target_function)

    @classmethod
    def tearDownClass(cls):
        for temp in [f for f in os.listdir('.') if f.startswith(cls.tempf)]:
            os.remove(temp)
        sys.stdout = cls.stdout
        sys.stderr = cls.stderr

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProperty)
    unittest.TextTestRunner(verbosity=2).run(suite)
