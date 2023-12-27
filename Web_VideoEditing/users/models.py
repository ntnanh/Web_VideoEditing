from django.db import models
from django.utils import timezone
from PIL import Image


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    create_at = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=50, default='client')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    
    class Meta:
        db_table = "users"
        
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(Users, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    