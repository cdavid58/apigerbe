from django.db import models

class Inventory(models.Model):
	code = models.CharField(unique=True, max_length=25,null = True, blank = True)
	code_int = models.CharField(unique=True, max_length=25,null = True, blank = True)
	name = models.CharField(unique = True,max_length= 80,null = True, blank = True)
	cost = models.CharField(max_length=25,null = True, blank = True)
	price_1 = models.CharField(max_length=25, null = True, blank = True)
	price_2 = models.CharField(max_length=25, null = True, blank = True)
	price_3 = models.CharField(max_length=25, null = True, blank = True)
	price_4 = models.CharField(max_length=25, null = True, blank = True)
	price_5 = models.CharField(max_length=25, null = True, blank = True)
	tax = models.CharField(max_length=3, null = True, blank = True)
	category = models.CharField(max_length = 80,null = True, blank = True)
	download = models.BooleanField(default=False)
	active = models.BooleanField(default=False)
	update = models.BooleanField(default=False)
	new_product = models.BooleanField(default=False)
	gerbe_1 = models.BooleanField(default=True) #gerge_1
	gerbe_2 = models.BooleanField(default=True) #gerge_2
	gerbe_3 = models.BooleanField(default=True) #gerge_3
	gerbe_4 = models.BooleanField(default=True) #gerge_4
	gerbe_5 = models.BooleanField(default=True) #gerge_5

	def __str__(self):
		return self.name +' | '+self.code