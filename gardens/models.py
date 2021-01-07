from django.db import models

class User(models.Model):
    pass
# waiting to see what users will look like from other team.

class Plant(models.Model):
    flower_name = models.CharField(max_length=30)
    cost = models.IntegerField()
    level = models.IntegerField()
    time_to_mature = models.IntegerField()
    exp_value = models.IntegerField()
    currency = models.IntegerField()
    desc = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.flower_name} {self.level} {self.desc}"


class Garden(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rows = models.IntegerField(default=2)
    columns = models.IntegerField(default=4)

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

