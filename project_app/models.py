from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Project(models.Model):
  
  #set the choices
  CATEGORY_CHOICES = [
    ('Planning', 'Planning'),
    ('Development', 'Development'),
    ('Strategy', 'Strategy'),
    ('Management', 'Management'),
    ('Marketing', 'Marketing')
  ]
  
  STATUS_CHOICES = [
    ('Not Started', 'Not Started'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed')
  ]
  
  PRIORITY_CHOICES = [
    ("Low", "Low"),
    ("Medium", "Medium"),
    ("High", "High"),
  ]
  
  
  #database
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=150)
  description = models.TextField()
  startdate = models.DateField()
  enddate = models.DateField()
  category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
  status = models.CharField(max_length=50, choices=STATUS_CHOICES)
  priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
  image1 = models.ImageField(upload_to='images/', default=None, null=True, blank=True)
  image2 = models.ImageField(upload_to='images/', default=None, null=True, blank=True)
  

  # Delete the images file from the filesystem
  def deleteImage1(self, *args, **kwargs):
    if self.image1:
      if os.path.isfile(self.image1.path):
        os.remove(self.image1.path)
    
  def deleteImage2(self, *args, **kwargs):
    if self.image2:
      if os.path.isfile(self.image2.path):
        os.remove(self.image2.path)
  
  
  
  def __str__(self):
    return f'{self.title} - {self.user.username}'