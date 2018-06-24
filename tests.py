import unittest

from flask_testing import LiveServerTestCase
from urllib2 import urlopen


class ServerTest(LiveServerTestCase):
    def server_is_up_and_running(self):
        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
