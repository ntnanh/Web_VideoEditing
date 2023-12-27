from django.db import models
from users.models import Users

# Create your models here.
class Subtitle(models.Model):
    path = models.FileField(upload_to='audio_files/')
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = "Subtitle"

class Upload(models.Model):
    path_video = models.FileField(upload_to='Files/')
    title_video = models.CharField(max_length=200, null=True)
    path_image = models.FileField(upload_to='Files/', null=True)
    
    class Meta:
        db_table = "Upload"


class UserUpload(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "UserUpload"
    
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    video_edit = models.FileField(upload_to='video_edits/')
    duration = models.IntegerField()
    format = models.CharField(max_length=50)
    size = models.IntegerField()
    update_date = models.DateTimeField()
    thumb = models.ImageField(upload_to='video_thumbs/')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    subtitle_id = models.ForeignKey(Subtitle, on_delete=models.CASCADE)
    upload_id = models.ForeignKey(Upload, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "Video"