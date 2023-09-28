from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    '''User model'''

    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    '''EmailVerification to store data about user's email'''

    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerify obj for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={
            'email': self.user.email,
            'code': self.code
        })
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Account confirmation for {self.user.username}'
        message = 'For account confirmation for {} follow the link {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() >= self.expiration else False


