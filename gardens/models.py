from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    current_level = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    current_balance = models.IntegerField(default=0)
    city = models.CharField(blank=True, max_length=150) #took out null attribute
    state = models.CharField(blank=True, max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    

    def __str__(self):
        return f"{self.user.username}, profile"

class Plant(models.Model):
    flower_name = models.CharField(max_length=30)
    cost = models.IntegerField()
    level = models.IntegerField()
    time_to_mature = models.IntegerField()
    exp_value = models.IntegerField()
    harvest_value = models.IntegerField()
    desc = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.flower_name} {self.level} {self.desc}"

# changed user to OneToOneField instead of foreign key. may have to change this back depending on functionality
class Garden(models.Model):
    rows = models.IntegerField(default=2)
    columns = models.IntegerField(default=4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='garden')

    def __str__(self):
        return f"Garden owned by User {self.user_id}"

class Plants_in_garden(models.Model):
    plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE)
    garden_id = models.ForeignKey(Garden, on_delete=models.CASCADE)
    harvested = models.BooleanField()
    watered = models.BooleanField()
    remaining_time = models.IntegerField()
    row_num = models.IntegerField()
    column_num = models.IntegerField()

    def __str__(self):
        return f"{self.plant_id} in {self.garden_id}"


