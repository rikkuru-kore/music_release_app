from django.db import models

# Create your models here.
class Items(models.Model):
    title = models.CharField(max_length=150)
    artist = models.CharField(max_length=150)
    text = models.TextField()
    level = models.IntegerField(null=True,blank=True)
    artwork = models.FileField(upload_to='artwork/',null=True,blank=True)
    price = models.PositiveIntegerField(default=300)
    tab = models.FileField(upload_to='tab/',null=True,blank=True)
    music = models.FileField(upload_to='music/',null=True,blank=True)
    image = models.FileField(upload_to='image/',null=True,blank=True)
    sale = models.PositiveIntegerField(null=True,blank=True,default=0)
    division = models.PositiveIntegerField()
    url = models.URLField(blank=True,null=True)
    volume = models.CharField(max_length=10)
    publish = models.BooleanField(default=False,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'items'
        
class Orders(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField()
    tentative_sale = models.CharField(max_length=150,blank=True,null=True)
    checkout_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        
class Inquiry(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    title = models.CharField(max_length=140,blank=True,null=True)
    text = models.TextField()
    reply = models.TextField(blank=True,null=True)
    is_replied = models.BooleanField(default=False,blank=True,null=True)
    checkout_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inquiry'
    