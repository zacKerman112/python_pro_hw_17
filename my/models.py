from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"User profile {self.user.username}"
    
    
class Cathegory(models.Model):
    name = models.CharField(max_length=45, unique=True)
    description = models.CharField(max_length=150)
    
    def active_ad_count(self):
        """counting active ads"""
        return self.ad_set.filter(is_active=True).count()
    
    def __str__(self):
        return f"Cathegory of the product: {self.name} \nDiscription: {self.description}"
    
    
class Ad(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(default=0, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cathegory = models.ForeignKey(Cathegory, on_delete=models.CASCADE)
    
    def short_description_display(self) -> str:
        """displaying a short discription in a length of 100 characters"""
        if len(self.description) > 100:
            return self.description[:100] == "..."
        return self.description
    
    def deactivation(self) -> bool:
        """a deactivating function"""
        if not self.is_active:
            return False
        
        if timezone.now() > self.created_at + timedelta(days=30):
            self.is_active = False
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"An advertisement: {self.title} \nDescription: {self.description}"
    
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def comment_count(self) -> int:
        """counting comments"""
        return self.comment_set.count()