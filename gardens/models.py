from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    current_level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    currency = models.IntegerField(default=100) # NEED TO GET STARTING BALANCE
    city = models.CharField(blank=True, null=True, max_length=150) #GET RID OF BLANK AND THEN REMIGRATE
    state = models.CharField(blank=True, null=True, max_length=150) #GET RID OF BLANK AND THEN REMIGRATE
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    

    def __str__(self):
        return f"{self.user.username}, profile"

# chrisrh
# p4ssw0rd