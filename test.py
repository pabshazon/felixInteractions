from .app import app
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testServerIsUp(self):
        response = self.app.get('/')
        assert b'Hello Felix!' in response.data

    def testIntentGreetings(self):
        response = self.app.get('/search?query=greetings')
        assert b'greeting' in response.data

# @todo tests for sessionId situations, arguments empty or nonexisting,

if __name__ == '__main__':
    unittest.main()