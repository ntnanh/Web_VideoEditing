from django.db import models
from django.utils import timezone

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    create_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, default='client')
    
    class Meta:
        db_table = "users"
        
    def __str__(self):
        return self.username
    
    empAuth_objects = models.Manager()
    