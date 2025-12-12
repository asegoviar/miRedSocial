from django.conf import settings
from django.test import TestCase


class ProjectStartupTest(TestCase):
    def test_project_starts(self):
        """
        El proyecto Django arranca correctamente.
        """
        self.assertIsNotNone(settings.SECRET_KEY)


class LoginPageTest(TestCase):
    def test_login_page_returns_200(self):
        """
        Test 2:
        La ruta /login responde con HTTP 200.
        """
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

class LoginTemplateTest(TestCase):
    def test_login_uses_correct_template(self):
        """
        Test 3:
        Verifica que la vista de login usa el template correcto.
        """
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "accounts/login.html")