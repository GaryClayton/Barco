from django.db import models

# Create your models here.


class Charity(models.Model):
    name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    overview = models.CharField(max_length=10000, blank=True)
    web = models.URLField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    number = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return str(self.id)


class CharityContact(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    comment = models.CharField(max_length=100, blank=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class CharityDonation(models.Model):
    date = models.DateField(blank=True, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=7, blank=True, default=0)
    comment = models.CharField(max_length=100, blank=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
