from django.db import models


class Bond(models.Model):
    user = models.ForeignKey("auth.User", related_name="bonds", on_delete=models.CASCADE)
    isin = models.CharField(max_length=100),
    size = models.IntegerField(),
    currency = models.CharField(max_length=3),
    maturity = models.DateField(),
    lei = models.CharField(max_length=100),
    legal_name = models.CharField(max_length=100)
