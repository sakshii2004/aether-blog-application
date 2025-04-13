from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.PositiveIntegerField(default=0)
    number_of_comments = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    liked_by = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def process_image(self):
        if self.image:
            image = Image.open(self.image)
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            width, height = image.size
            min_side = min(width, height)
            left = (width - min_side) / 2
            top = (height - min_side) / 2
            right = (width + min_side) / 2
            bottom = (height + min_side) / 2
            image = image.crop((left, top, right, bottom))

            image = image.resize((640, 640))

            buffer = BytesIO()
            image.save(buffer, format='JPEG')
            self.image = InMemoryUploadedFile(buffer, 'ImageField', self.image.name, 'image/jpeg', buffer.tell(), None)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.body
