from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    profUser = models.OneToOneField(User, on_delete=models.CASCADE)
    profPic = models.ImageField(upload_to='public/', default='default.jpg')
    email = models.EmailField(unique=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, blank=True)

    def __str__(self):
        return str(self.profUser)
