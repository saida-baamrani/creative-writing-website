from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.db.models import Count



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Nationality= models.CharField(max_length=30, blank=True)
    image=models.FileField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Genre(models.Model):
	genre= models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.genre

class Language(models.Model):
	langue= models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.langue

class Story(models.Model):
     title = models.CharField(max_length=100)
     resume = models.TextField(max_length=500)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     genres = models.ManyToManyField(Genre ,blank=True ,null=True)
     langues = models.ManyToManyField(Language ,blank=True ,null=True)
     image=models.FileField(blank=True)

     @property
     def get_chapter(self):
     	chapter=Chapter.objects.filter(story=self.id).values()
     	return chapter
     def count_chapters(self):
        number=Chapter.objects.filter(story=self.id).count()
        return number
     def get_comments(self):
     	comments=Comments.objects.filter(story=self.id).values()
     	return comments

     def get_absolute_url(self):
        return reverse('add-chapter', kwargs={'pk': self.pk})

class Chapter(models.Model):
    title_chap=models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    def get_story(self):
        st=self.story.id
        
        return st

      
    




class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

	
	
		
