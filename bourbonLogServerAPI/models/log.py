from django.db import models

class Log(models.Model):

    logger = models.ForeignKey("Logger", on_delete=models.CASCADE)
    recordCreation = models.DateField(default="0000-00-00",)
    bourbonName = models.CharField(max_length=50)
    distiller = models.CharField(max_length=50)
    proof = models.CharField(max_length=50)
    age = models.CharField(max_length=50)
    batchNum = models.CharField(max_length=50)
    owned = models.CharField(max_length=50)                 #<-make this customer property. reference JOINED in levelup events?
    rating = models.CharField(max_length=50)
    post_image_url = models.CharField(max_length=200)       #<-do this differently. Open from local folder. Users don't want to paste url's