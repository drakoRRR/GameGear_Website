from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


# Create your tests here.
class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.data = {
            'first_name': 'John', 'last_name': 'Pegua',
            'username': 'bob1ik', 'email': 'example@gmail.com',
            'password1': 'qwerty123', 'password': 'qwerty123'
        }
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register_page.html')

    def test_user_registration_post(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # create user
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTrue(User.objects.filter(username=username).exists())

        # check create email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertEquals(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=24)).date()
        )

