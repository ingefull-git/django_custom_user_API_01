from django.db import models


class Client(models.Model):

    fname       = models.CharField(verbose_name="first name", max_length=100, blank=True, null=True)
    lname       = models.CharField(verbose_name="last name", max_length=100, blank=False, null=False)
    email       = models.EmailField(verbose_name="email", blank=False, null=False)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    @property
    def fullname(self):
        return f'{self.fname} {self.lname}'

    def __str__(self):
        return self.fullname