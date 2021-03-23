from django.db import models

class Log(models.Model):

    logger = models.ForeignKey("Logger", on_delete=models.CASCADE)
    bourbon_name = models.CharField(max_length=50)
    distiller = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    proof = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    batch_num = models.CharField(max_length=50)
    owned = models.BooleanField()                 
    rating = models.CharField(max_length=50)
    notes = models.CharField(max_length=200)