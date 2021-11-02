import unittest

from .api_user.tests import ApiUserTest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ApiUserTest)
    unittest.TextTestRunner().run(suite)