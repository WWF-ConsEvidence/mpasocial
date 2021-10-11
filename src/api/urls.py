from django.urls import path
from rest_framework import routers
from .resources.views import *

router = routers.DefaultRouter()

router.register("birth", ListBirth, "birth")
router.register("country", ListCountry, "country")
router.register("death", ListDeath, "death")
router.register("demographic", ListDemographic, "demographic")
router.register("monitoringstaff", ListMonitoringStaff, "monitoringstaff")
router.register("fgd", ListFGD, "fgd")
router.register("globalstep", ListGlobalStep, "globalstep")
router.register("globalthreat", ListGlobalThreat, "globalthreat")
router.register("habitat", ListHabitat, "habitat")
router.register("habitatrule", ListHabitatRule, "habitatrule")
router.register("household", ListHousehold, "household")
router.register("kii", ListKII, "kii")
router.register("localstep", ListLocalStep, "localstep")
router.register("localthreat", ListLocalThreat, "localthreat")
router.register(
    "marineorganizationmembership",
    ListMarineOrganizationMembership,
    "marineorganizationmembership",
)
router.register("mpa", ListMPA, "mpa")
router.register(
    "nonmarineorganizationmembership",
    ListNonMarineOrganizationMembership,
    "nonmarineorganizationmembership",
)
router.register("right", ListRight, "right")
router.register("rule", ListRule, "rule")
router.register("settlement", ListSettlement, "settlement")
router.register("species", ListSpecies, "species")
router.register("speciesrule", ListSpeciesRule, "speciesrule")
router.register("stakeholder", ListStakeholder, "stakeholder")
router.register("zone", ListZone, "zone")

urlpatterns = [path("lookups", LookupsListView.as_view())] + router.urls

swagger_urls = [
    u
    for u in urlpatterns
    if u.name is None
    or (not u.name.endswith("-json") and not u.name.endswith("-detail"))
]
