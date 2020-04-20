from django.db import models

# Create your models here.


class Product(models.Model):
	id = models.AutoField(primary_key=True)
	keyword = models.CharField(max_length=255)
	image = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	link = models.CharField(max_length=255)
	rating = models.CharField(max_length=50)
	price = models.CharField(max_length=50)

class AutoSuggestion(models.Model):
	id = models.AutoField(primary_key=True)
	keyword = models.CharField(max_length=100)
	suggesstion = models.CharField(max_length=200)

