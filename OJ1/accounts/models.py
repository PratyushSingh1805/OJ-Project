from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    #profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True, null=True)
    is_problem_setter = models.BooleanField(default=False)
    #profile_pic = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    from .models import UserProfile
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Optional: update fields if needed
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()
