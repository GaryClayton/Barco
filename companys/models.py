from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class Company(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=60, blank=True)
    subsector = models.CharField(max_length=60, blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    web = models.URLField(blank=True)

    def __str__(self):
        return str(self.id)


class CompanyContact(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=60, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    emailconsent = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class ClubContact(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class CRM(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return str(self.id)
