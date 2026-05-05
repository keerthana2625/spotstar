from django.db import models

class User(models.Model):
    ROLE_CHOICES = (
        ('listener', 'Listener'),
        ('uploader', 'Uploader'),
    )

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Media(models.Model):
    MEDIA_TYPE = (
        ('audio', 'Audio'),
        ('video', 'Video'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=150)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE)

    music_director = models.CharField(max_length=100, blank=True)
    singer = models.CharField(max_length=100, blank=True)

    director = models.CharField(max_length=100, blank=True)
    actor = models.CharField(max_length=100, blank=True)
    actress = models.CharField(max_length=100, blank=True)

    release_year = models.IntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    file = models.FileField(upload_to='media/')
    thumbnail = models.FileField(upload_to='thumbnails/', null=True, blank=True)
    uploaded_by = models.CharField(max_length=50)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Like(models.Model):
    user_name = models.CharField(max_length=50)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_name', 'media')

class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Playlist(models.Model):
    user_name = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    media_items = models.ManyToManyField(Media, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)