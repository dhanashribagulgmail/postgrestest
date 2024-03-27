from django.db import models

from django.contrib.auth.models import User 

# Create your models here.


class donar_details(models.Model):
    #id=models.AutoField()

    user=models.ForeignKey(User , on_delete=models.SET_NULL ,null=True ,blank=True )
    name= models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()
    address=models.TextField(null=True, blank =True)
    donar_photo=models.ImageField(upload_to="donar_details" ,null=True)






 


