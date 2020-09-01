from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse_lazy,reverse
from django.db.models.signals import post_save

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, default = 1, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    slug = models.SlugField(null=True, unique=True) 
    content=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
    favorite = models.ManyToManyField(User,related_name='favorite',blank= True)
    def __str__(self):
        return self.title+ ' ' + self.content
    def get_absolute_url(self):
        return reverse('note-detail',  args=[str(self.id)])
    class Meta:
    	ordering=('-publish',) 


class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=True)
    birthday=models.DateField(blank=True,null=True) 
    bio=models.TextField(blank=True,null=True)
    profilepic = models.ImageField(upload_to='users/', blank=True, null=True)
    hobby = models.CharField(max_length=40, blank=True, null=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)