from django.db import models

class FlavorSum(models.Model):

    flavor = models.ForeignKey("Flavor", on_delete=models.CASCADE)
    flavorweight = models.IntegerField()
    log = models.ForeignKey("Log", on_delete=models.CASCADE)
 