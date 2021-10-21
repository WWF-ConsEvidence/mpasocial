from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserProfileForm
from .models import *


UserModel = get_user_model()
admin.site.unregister(UserModel)


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
class FGDSurveyVersionAdmin(admin.ModelAdmin):
    list_display = ["id", "version"]


@admin.register(HouseholdSurveyVersion)
class HouseholdSurveyVersionAdmin(admin.ModelAdmin):
    list_display = ["id", "version"]


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


admin.site.register(Country)
admin.site.register(Death)
admin.site.register(Demographic)
admin.site.register(FGD)
admin.site.register(GlobalStep)
admin.site.register(GlobalThreat)
admin.site.register(Habitat)
admin.site.register(HabitatRule)
admin.site.register(KII)
admin.site.register(LocalStep)
admin.site.register(LocalThreat)
admin.site.register(MarineOrganizationMembership)
admin.site.register(MPA)
admin.site.register(NonMarineOrganizationMembership)
admin.site.register(Right)
admin.site.register(Rule)
admin.site.register(Species)
admin.site.register(SpeciesRule)
admin.site.register(Stakeholder)
admin.site.register(Zone)
