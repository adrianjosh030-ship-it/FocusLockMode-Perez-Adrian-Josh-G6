from django.test import TestCase
from django.urls import reverse

from .models import User

PW = "Str0ng-Pass!234"


class AccountTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("boss", "boss@example.com", PW, role=User.Role.ADMIN)
        self.student = User.objects.create_user("mia", "mia@example.com", PW)

    def reg(self, **over):
        data = {"username": "new", "first_name": "N", "last_name": "U", "email": "new@example.com",
                "contact_number": "09171234567", "password1": PW, "password2": PW}
        data.update(over)
        return self.client.post(reverse("accounts:register"), data)

    def test_register_ok_and_hashed(self):
        r = self.reg()
        self.assertRedirects(r, reverse("accounts:login"))
        u = User.objects.get(username="new")
        self.assertEqual(u.role, User.Role.STUDENT)
        self.assertNotEqual(u.password, PW)
        self.assertTrue(u.password.startswith("pbkdf2_"))

    def test_register_validation(self):
        self.assertEqual(User.objects.filter(username="new").count(), 0)
        self.reg(email="MIA@example.com")
        self.reg(email="not-an-email")
        self.reg(password2="different")
        self.reg(username="mia", email="other@example.com")
        self.reg(first_name="")
        self.assertEqual(User.objects.count(), 2)

    def test_login_logout(self):
        r = self.client.post(reverse("accounts:login"), {"username": "mia", "password": "bad"})
        self.assertContains(r, "Invalid username or password.")
        r = self.client.post(reverse("accounts:login"), {"username": "mia", "password": PW})
        self.assertRedirects(r, reverse("accounts:dashboard"), fetch_redirect_response=False)
        self.client.post(reverse("accounts:logout"))
        r = self.client.get(reverse("accounts:profile"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("accounts:login"), r.url)

    def test_role_routing_and_isolation(self):
        self.client.login(username="mia", password=PW)
        r = self.client.get(reverse("accounts:dashboard"), follow=False)
        self.assertRedirects(r, reverse("accounts:student_dashboard"))
        r = self.client.get(reverse("accounts:admin_dashboard"))
        self.assertRedirects(r, reverse("accounts:dashboard"), fetch_redirect_response=False)
        self.client.login(username="boss", password=PW)
        self.assertEqual(self.client.get(reverse("accounts:admin_dashboard")).status_code, 200)
        r = self.client.get(reverse("accounts:student_dashboard"))
        self.assertEqual(r.status_code, 302)

    def test_profile_update_own_only(self):
        self.client.login(username="mia", password=PW)
        r = self.client.post(reverse("accounts:profile_edit"), {
            "first_name": "Mia", "last_name": "L", "email": "mia2@example.com", "contact_number": "0917 123 4567"})
        self.assertRedirects(r, reverse("accounts:profile"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.email, "mia2@example.com")
        # cannot take another user's email
        r = self.client.post(reverse("accounts:profile_edit"), {
            "first_name": "Mia", "last_name": "L", "email": "boss@example.com"})
        self.assertEqual(r.status_code, 200)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.email, "boss@example.com")
