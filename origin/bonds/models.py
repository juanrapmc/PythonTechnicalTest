from django.db import models
from bonds.utils import getLeiLegalName
from rest_framework.exceptions import ValidationError


class Bond(models.Model):
    user = models.ForeignKey("auth.User", related_name="bonds", on_delete=models.CASCADE)
    isin = models.CharField(max_length=100, null=False)
    size = models.IntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=100)
    legal_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        legal_name = getLeiLegalName(self.lei)
        if legal_name:
            self.legal_name = legal_name
        else:
            raise ValidationError
        super(Bond, self).save(*args, **kwargs)
