import unittest
from urllib2 import urlopen

from flask_testing import LiveServerTestCase


class ServerTest(LiveServerTestCase):
    def test_server_is_up_and_running(self):
        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
