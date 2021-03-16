from django.db import models

class Flavor(models.Model):

    flavor = models.CharField(max_length=50)
    
