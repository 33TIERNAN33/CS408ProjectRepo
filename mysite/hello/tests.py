from django.test import TestCase

# Create your tests here.
class HelloWorldTests(TestCase):
    def test_home_page_renders_hello_world(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello World")
