from django.db import models
from django.contrib.auth.models import AbstractUser

class Tiers:
    free = 'Free'
    basic = 'Basic'
    premium = 'Premium'

class User(AbstractUser):
    tier_choices = (
        (Tiers.free, 'Free'),
        (Tiers.basic, 'Basic'),
        (Tiers.premium, 'Premium'),
    )

    tier = models.CharField(max_length=10, choices=tier_choices, default=Tiers.free)
