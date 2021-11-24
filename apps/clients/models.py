from django.db import models


class Status(models.TextChoices):
        OK = 1, "Ok"
        WARNING = 2, "Warning"
        ERROR = 3, "Error"

class Client(models.Model):
    psid        = models.CharField(max_length=10, unique=True, blank=True, null=True)
    fname       = models.CharField(verbose_name="first name", max_length=100, blank=True, null=True)
    lname       = models.CharField(verbose_name="last name", max_length=100, blank=False, null=False)
    email       = models.EmailField(verbose_name="email", blank=False, null=False)
    status      = models.CharField(max_length=50, choices=Status.choices, default=Status.OK)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    @property
    def fullname(self):
        return f'{self.fname} {self.lname}'

    def __str__(self):
        return self.fullname

class Invoice(models.Model):

    code        = models.CharField(max_length=10, blank=True, unique=True)
    client      = models.ForeignKey(Client, on_delete=models.CASCADE)
    date        = models.DateField(auto_now=True)
    amount      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(None)
            number = f'{self.pk:06}'
            self.code = "INV-" + number
        super().save(*args, **kwargs)


