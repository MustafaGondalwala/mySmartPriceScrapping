from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
	id = models.AutoField(primary_key=True)
	keyword = models.CharField(max_length=255)
	image = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	link = models.CharField(max_length=255,unique=True)
	rating = models.CharField(max_length=50)
	price = models.CharField(max_length=50)
	page = models.IntegerField();
	created_at = models.DateField(default=timezone.now)



class ProductDescription(models.Model):	
	id = models.AutoField(primary_key=True)
	link = models.CharField(max_length=255,unique=True)
	store = models.TextField()
	all_images = models.TextField()
	description = models.TextField()
	title = models.CharField(max_length=100)
	rating = models.CharField(max_length=10)
	bullets = models.TextField()
	links = models.TextField()
	product_link_json = models.TextField()
	created_at = models.DateField(default=timezone.now)


class ProductLinks(models.Model):	
	id = models.AutoField(primary_key=True)
	link = models.CharField(max_length=255,unique=True)
	product_link_json = models.TextField()
	created_at = models.DateField(default=timezone.now)



class AutoSuggestion(models.Model):
	id = models.AutoField(primary_key=True)
	keyword = models.CharField(max_length=100)
	suggesstion = models.CharField(max_length=200)


