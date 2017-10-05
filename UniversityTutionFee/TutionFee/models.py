from django.db import models


class Information(models.Model):
    u_name = models.CharField(max_length=200)
    url = models.URLField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.u_name


class Cost(models.Model):
    u_name = models.ForeignKey(Information)
    subject = models.CharField(max_length=50)
    cost = models.IntegerField()

    def __str__(self):
        return self.cost

    # pass:tuhin123


