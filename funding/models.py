from django.db import models

# Create your models here.
class Goods(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=30)
    detail = models.CharField(max_length=255)
    goal = models.PositiveIntegerField(blank=True, null=True)
    date_limit = models.DateField()
    price_per_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods'
