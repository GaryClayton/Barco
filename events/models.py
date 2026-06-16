from django.db import models

import companys.models

# Create your models here.


class Events(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=60, blank=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Contribution(models.Model):
    support = models.CharField(max_length=60)
    value = models.DecimalField(decimal_places=2, max_digits=7, blank=True, default=0)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    company = models.ForeignKey(companys.models.Company, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
