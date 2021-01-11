from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

from gardens.models import Game, Garden

User = get_user_model()

# user = User.objects.get(pk=1)

# user.save()
# post_save

@receiver(post_save, sender=User)
def create_game_profile(sender, instance, created, **kwargs):
    # sender = <class User>
    # instance =  <User: chrisrh>
    # created = True
    if created: # initial User.save() -- first creation
        # This logic only runs if User.save() happened
        # And only if created was True. (User is brand new)
        # I want to create a Game instance
        # then attach it to `instance` which is the current user instance.
        game = Game.objects.create(user=instance)
        instance.profile = game
        instance.profile.save()

@receiver(post_save, sender=User)
def create_game_garden(sender, instance, created, **kwargs):
    # sender = <class User>
    # instance =  <User: chrisrh>
    # created = True
    if created: # initial User.save() -- first creation
        # This logic only runs if User.save() happened
        # And only if created was True. (User is brand new)
        # I want to create a Garden instance
        # then attach it to `instance` which is the current user instance.
        garden = Garden.objects.create(user=instance)
        instance.garden = garden
        instance.garden.save()
