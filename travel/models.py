from django.db import models

# Create your models here.
# class ImageStore(models.Model):
	# name = models.CharField(max_length=150,null=True)
	# img = models.ImageField(upload_to='img')
	# def __unicode__(self):
        # return self.name
# class Meta:
	# db_table = 'ImageStore'

class Account(models.Model):
	EmailAddress = models.EmailField(primary_key=True)
	Key = models.CharField(max_length=30)
	def __unicode__(self):
		return self.EmailAddress

class User(models.Model):
	EmailAddress = models.ForeignKey(Account)
	Name = models.CharField(max_length=30)
	Gender = models.CharField(max_length=10)
	Age = models.IntegerField()
	Email = models.EmailField()
	
	Silence = models.BooleanField()
	Active = models.BooleanField()
	Chat = models.BooleanField()
	MissPast = models.BooleanField()
	Discription = models.CharField(max_length = 80)
	def __unicode__(self):
		return self.Name

class Place(models.Model):
	Order = models.IntegerField()
	EmailAddress = models.ForeignKey(Account)
	Place = models.CharField(max_length=30)
	Comment = models.TextField()
	Number = models.CharField(max_length=20)
	def __unicode__(self):
		return self.Place

class Team(models.Model):
	Owner = models.ForeignKey(Account)
	Province = models.CharField(max_length=30)
	City = models.CharField(max_length=30)
	Date = models.DateField()
	mem = models.ManyToManyField(User)
	def __unicode__(self):
		return str(self.Owner)

class Willgo(models.Model):
	EmailAddress = models.ForeignKey(User)
	From = models.CharField(max_length=20)
	Province = models.CharField(max_length=20)
	City = models.CharField(max_length=20)
	Date = models.DateField()
	Time = models.IntegerField()
	Low = models.DecimalField(max_digits=6, decimal_places=0)
	High = models.DecimalField(max_digits=6, decimal_places=0)
	Status = models.CharField(max_length=20)
	def __unicode__(self):
		return self.City