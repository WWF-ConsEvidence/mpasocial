from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Household, UserProfile
from utils import upsert_mpa_interviewyear


@receiver(post_save, sender=get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        up = instance.profile
    except get_user_model().profile.RelatedObjectDoesNotExist:
        UserProfile.objects.create(user=instance)
    instance.profile.save()


# def update_mpa_interviewyears(sender, instance, created, **kwargs):
#     mpa = instance.mpa  # TODO: handle FGD, KII
#     year = instance.interviewyear
#     upsert_mpa_interviewyear(mpa, year)
#
#
# post_save.connect(
#     update_mpa_interviewyears,
#     sender=Household,
#     dispatch_uid=f"{Household._meta.object_name}_update_mpa_interviewyears",
# )
