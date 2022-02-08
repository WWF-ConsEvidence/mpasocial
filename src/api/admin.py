from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserProfileForm
from .models import *


UserModel = get_user_model()
admin.site.unregister(UserModel)

fields_to_ignore = ['created_on', 'updated_on', 'updated_by']


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name not in fields_to_ignore]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class LookupAdmin(admin.ModelAdmin):
    list_display = ["code", "bahasaindonesia", "english"]
    ordering = ["code", "bahasaindonesia", "english"]


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


@admin.register(UserModel)
class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

    def save_formset(self, request, form, formset, change):
        formset.save()
        for f in formset.forms:
            obj = f.instance
            obj.updated_by = request.user
            obj.save()


@admin.register(FGDSurveyVersion)
class FGDSurveyVersionAdmin(CustomModelAdmin):
    pass


@admin.register(HouseholdSurveyVersion)
class HouseholdSurveyVersionAdmin(CustomModelAdmin):
    pass


@admin.register(KIISurveyVersion)
class KIISurveyVersionAdmin(admin.ModelAdmin):
    list_display = ["id", "version"]


@admin.register(Birth)
class BirthAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Birth._meta.get_fields()]


@admin.register(MonitoringStaff)
class MonitoringStaffAdmin(admin.ModelAdmin):
    list_display = ["staffid", "name"]


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ["householdid", "kkcode"]


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):
    list_display = ["name", "districtname", "mpa"]
    ordering = ["name", "districtname", "mpa"]


@admin.register(MPANetwork)
class MPANetworkAdmin(LookupAdmin):
    pass


@admin.register(Seascape)
class SeascapeAdmin(LookupAdmin):
    pass


@admin.register(LkpAssetAssistance)
class LkpAssetAssistanceAdmin(LookupAdmin):
    pass


@admin.register(LkpAssetObtain)
class LkpAssetObtainAdmin(LookupAdmin):
    pass


@admin.register(LkpFreqFishTime)
class LkpFreqFishTimeAdmin(LookupAdmin):
    pass


@admin.register(LkpFishTechCategory)
class LkpFishTechCategoryAdmin(LookupAdmin):
    pass


@admin.register(LkpFishTechnique)
class LkpFishTechniqueAdmin(LookupAdmin):
    list_display = [
        "code",
        "bahasaindonesia",
        "english",
        "consolidatedfishtechcategory",
    ]


@admin.register(LkpLivelihood)
class LkpLivelihoodAdmin(LookupAdmin):
    pass


@admin.register(LkpNoneToAllScale)
class LkpNoneToAllScaleAdmin(LookupAdmin):
    pass


@admin.register(Users)
class UsersAdmin(CustomModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(CustomModelAdmin):
    pass

@admin.register(Death)
class DeathAdmin(CustomModelAdmin):
    pass

@admin.register(Demographic)
class DemographicAdmin(CustomModelAdmin):
    pass


@admin.register(FGD)
class FGDAdmin(CustomModelAdmin):
    pass


@admin.register(GlobalStep)
class GlobalStepAdmin(CustomModelAdmin):
    pass


@admin.register(GlobalThreat)
class GlobalThreatAdmin(CustomModelAdmin):
    pass


@admin.register(Habitat)
class HabitatAdmin(CustomModelAdmin):
    pass


@admin.register(HabitatRule)
class HabitatRuleAdmin(CustomModelAdmin):
    pass


@admin.register(KII)
class KIIAdmin(CustomModelAdmin):
    pass


@admin.register(LocalStep)
class LocalStepAdmin(CustomModelAdmin):
    pass


@admin.register(LocalThreat)
class LocalThreatAdmin(CustomModelAdmin):
    pass


@admin.register(MarineOrganizationMembership)
class MarineOrganizationMembershipAdmin(CustomModelAdmin):
    pass


@admin.register(MPA)
class MPAAdmin(CustomModelAdmin):
    pass


@admin.register(NonMarineOrganizationMembership)
class NonMarineOrganizationMembershipAdmin(CustomModelAdmin):
    pass


@admin.register(Right)
class RightAdmin(CustomModelAdmin):
    pass


@admin.register(Rule)
class RuleAdmin(CustomModelAdmin):
    pass


@admin.register(Species)
class SpeciesAdmin(CustomModelAdmin):
    pass


@admin.register(SpeciesRule)
class SpeciesRuleAdmin(CustomModelAdmin):
    pass


@admin.register(Stakeholder)
class StakeholderAdmin(CustomModelAdmin):
    pass


@admin.register(Zone)
class ZoneAdmin(CustomModelAdmin):
    pass

