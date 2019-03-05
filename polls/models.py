from django.db import models
import os
import uuid
# Create your models here.


def user_path(instance,filename):
    b=os.path.join("img",str(instance.user_id), str(filename))
    print(b)
    return os.path.join("img",str(instance.user_id), str(filename))

def food_path(instance,filename):
    b=os.path.join("img",str(instance.upload_user.user_id),"food", str(filename))
    print(b)
    return os.path.join("img",str(instance.upload_user.user_id),"food", str(filename))

class User_info(models.Model):
    img = models.ImageField(upload_to=user_path,default="")
    user_id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=100)
    user_password=models.CharField(max_length=100)
    phone_num=models.CharField(max_length=100,default="No")
    address=models.CharField(max_length=100,default="No")
    #pub_date = models.DateTimeField('date published')

class Food_info(models.Model):
    food_img = models.ImageField(upload_to=food_path,default="")
    upload_user = models.ForeignKey(User_info, on_delete=models.CASCADE)
    food_id=models.AutoField(primary_key=True)
    food_name=models.CharField(max_length=100)
    food_price=models.FloatField(default=0)
    food_quantity=models.IntegerField(default=0)
    food_intro_text=models.CharField(max_length=10000,default="No introduction")

class Order(models.Model):
    buyer=models.ForeignKey(User_info,on_delete=models.DO_NOTHING,related_name='buy_order')
    food_id=models.CharField(max_length=100,default='')
    food_name=models.CharField(max_length=100)
    food_num=models.IntegerField(default=0)
    food_price=models.FloatField(default=0)
    cost=models.FloatField(default=0)
    seller=models.ForeignKey(User_info,on_delete=models.DO_NOTHING,related_name="sell_order")
    has_pay=models.BooleanField(default=False)
    has_complete=models.BooleanField(default=False)
    can_buy=models.BooleanField(default=False)

class Raw_material(models.Model):
    related_food=models.ForeignKey(Food_info, on_delete=models.CASCADE)
    material_id=models.AutoField(primary_key=True)
    material_name=models.CharField(max_length=100)
    material_quantity=models.CharField(max_length=100)

class Process(models.Model):
    step_num=models.IntegerField()
    step_text=models.CharField(max_length=1000)