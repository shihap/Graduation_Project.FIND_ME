from django.db import models
from datetime import date, datetime


# Create your models here.

 


class user(models.Model):
    user_name = models.CharField(max_length=45,null=False,default='')
    password = models.CharField(max_length=45,null=False,default='')
    email = models.CharField(max_length=45,null=False,default='',unique=True)
    profile_picture = models.CharField(max_length=1000,null=True,default=None,unique=True)
    location = models.CharField(max_length=45,null=True,default=None)
    phone = models.CharField(max_length=45,null=False,default='',unique=True)



class relatives(models.Model):
    relative = models.ForeignKey(user, on_delete=models.CASCADE,null=False,related_name='relative_id')
    user = models.ForeignKey(user, on_delete=models.CASCADE,null=False,related_name='user_id')
    

class requests(models.Model):
    sender = models.ForeignKey(user, on_delete=models.CASCADE,null=False,related_name='sender_id')
    reciver = models.ForeignKey(user, on_delete=models.CASCADE,null=False,related_name='reciver_id')


class images_dataset(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE,null=False)
    image = models.ImageField(upload_to='photos',null=True)
    

class post(models.Model):
    description = models.CharField(max_length=1000,default=None,null=True)
    datetime = models.DateTimeField(null=False,default=datetime.now())
    type = models.CharField(max_length=45,null=False)
    user = models.ForeignKey(user, on_delete=models.CASCADE , null=False)
    image_dir = models.CharField(max_length=1000, null=False)
    image_view = models.CharField(max_length=1000, null=False,default='')
    location = models.CharField(max_length=100, null=False,default='')
    case = models.CharField(max_length=45, null=False,default='')


class notfications(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE,null=False)
    smallDescription = models.CharField(max_length=1000,null=False,default='')
    date = models.DateTimeField(null=False,default=datetime.now())
    









'''

class Car(models.Model):

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6,decimal_places=2)


    class Meta:

        ordering = ['name']
        verbose_name = 'new_car'
	    


    def __str__(self):
	    return self.name
   

'''   