from django.apps import AppConfig

# from tracker.models import *
# from tracker.signals import *


class TrackerConfig(AppConfig):
    name = 'tracker'

    # def ready(self):
    #     post_save.connect(add_referral_points, sender=Contract)
