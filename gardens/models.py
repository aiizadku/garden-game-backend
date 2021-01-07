from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    current_level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    currency = models.IntegerField(default=0)
    city = models.CharField(blank=True, max_length=150) #took out null attribute
    state = models.CharField(blank=True, max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    

    def __str__(self):
        return f"{self.user.username}, profile"

# chrisrh
# p4ssw0rd