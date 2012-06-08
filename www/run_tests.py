import unittest
from test import all_tests

testSuite = all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)