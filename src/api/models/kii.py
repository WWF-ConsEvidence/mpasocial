from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from .base import (
    NODATA,
    SKIP_CODES,
    YES_NO_CHOICES,
    MAX_YEAR,
    YEAR_CHOICES,
    KII_FREQ_CHOICES,
    MinValueBCValidator,
    MaxValueBCValidator,
    BaseModel,
    MonitoringStaff,
    Settlement,
)
from .fgd import FGD


class KIISurveyVersion(BaseModel):
    version = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("version",)

    def __str__(self):
        return self.version


class KII(BaseModel):
    kiiid = models.IntegerField(primary_key=True)
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT)
    kiicode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    fgd = models.ForeignKey(FGD, on_delete=models.SET_NULL, null=True, blank=True)
    keyinformantrole = models.CharField(max_length=255, default=str(NODATA[0]))
    primaryinterviewer = models.ForeignKey(
        MonitoringStaff, on_delete=models.PROTECT, related_name="kii_primaryinterviewer"
    )
    secondaryinterviewer = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.PROTECT,
        related_name="kii_secondaryinterviewer",
        default=NODATA[0],
    )
    kiidate = models.DateField(blank=True, null=True)
    yearmonitoring = models.PositiveSmallIntegerField(
        choices=YEAR_CHOICES,
        validators=[MinValueBCValidator(2000), MaxValueBCValidator(MAX_YEAR)],
        default=NODATA[0],
    )
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    kiiversion = models.ForeignKey(KIISurveyVersion, on_delete=models.PROTECT)
    mpahistoryl = models.TextField(default=str(NODATA[0]))
    mpahistory = models.TextField(default=str(NODATA[0]))
    pilotnzones = models.PositiveSmallIntegerField(default=NODATA[0])
    ecozone = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    soczone = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    druleeco = models.PositiveSmallIntegerField(
        choices=KII_FREQ_CHOICES, default=NODATA[0]
    )
    drulesoc = models.PositiveSmallIntegerField(
        choices=KII_FREQ_CHOICES, default=NODATA[0]
    )
    pilotnestedness = models.CharField(max_length=255, default=str(NODATA[0]))
    rulecomml = models.TextField(default=str(NODATA[0]))
    rulecomm = models.TextField(default=str(NODATA[0]))
    ruleawarel = models.TextField(default=str(NODATA[0]))
    ruleaware = models.TextField(default=str(NODATA[0]))
    rulepracticel = models.TextField(default=str(NODATA[0]))
    rulepractice = models.TextField(default=str(NODATA[0]))
    informalrulel = models.TextField(default=str(NODATA[0]))
    informalrule = models.TextField(default=str(NODATA[0]))
    ruleparticipationl = models.TextField(default=str(NODATA[0]))
    ruleparticipation = models.TextField(default=str(NODATA[0]))
    monitorl = models.TextField(default=str(NODATA[0]))
    monitor = models.TextField(default=str(NODATA[0]))
    penverbal = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penwritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penfines = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penincarceraton = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    penotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    penfreq = models.PositiveSmallIntegerField(
        choices=KII_FREQ_CHOICES, default=NODATA[0]
    )
    penprevious = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    peneco = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES, default=NODATA[0])
    penecon = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    pensoc = models.PositiveSmallIntegerField(choices=YES_NO_CHOICES, default=NODATA[0])
    penwealth = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penpower = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penstatus = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penfactorother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penfactorotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    penfactorotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    incened = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenskills = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenpurchase = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenloan = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenpayment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenemploy = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    incenotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    incenotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    ecomonverbal = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonwritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonposition = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonfine = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonincarceration = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    ecomonotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    ecomonotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    socmonverbal = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonwritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonposition = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonfine = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonincarceration = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socmonotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    socmonotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    compmonverbal = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonwritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonposition = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonfine = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonincarceration = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    compmonotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    compmonotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    penmonverbal = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonwritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonposition = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonfine = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonincarceration = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penmonotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    penmonotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    conflictresl = models.TextField(default=str(NODATA[0]))
    conflictres = models.TextField(default=str(NODATA[0]))
    ecoimpactl = models.TextField(default=str(NODATA[0]))
    ecoimpact = models.TextField(default=str(NODATA[0]))
    socimpactl = models.TextField(default=str(NODATA[0]))
    socimpact = models.TextField(default=str(NODATA[0]))
    contributionl = models.TextField(default=str(NODATA[0]))
    contribution = models.TextField(default=str(NODATA[0]))
    benefitl = models.TextField(default=str(NODATA[0]))
    benefit = models.TextField(default=str(NODATA[0]))
    ecoimpactcovidl = models.TextField(default=str(NODATA[0]))
    ecoimpactcovid = models.TextField(default=str(NODATA[0]))
    socimpactcovidl = models.TextField(default=str(NODATA[0]))
    socimpactcovid = models.TextField(default=str(NODATA[0]))
    mpaimpactcovidl = models.TextField(default=str(NODATA[0]))
    mpaimpactcovid = models.TextField(default=str(NODATA[0]))
    anyotherinfol = models.TextField(default=str(NODATA[0]))
    anyotherinfo = models.TextField(default=str(NODATA[0]))
    anyotherkil = models.TextField(default=str(NODATA[0]))
    anyotherki = models.TextField(default=str(NODATA[0]))
    anyotherdocsl = models.TextField(default=str(NODATA[0]))
    anyotherdocs = models.TextField(default=str(NODATA[0]))
    notesl = models.TextField(default=str(NODATA[0]))
    notes = models.TextField(default=str(NODATA[0]))
    dataentryid = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kii_staff_data_entry",
    )
    datacheck = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="kii_staff_data_check",
    )
    violationfreq = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )


    @property
    def mpa(self):
        return self.settlement.mpa.mpaid

    class Meta:
        verbose_name = _("KII")
        verbose_name_plural = _("KIIs")

    def __str__(self):
        return str(self.pk)


class HabitatRule(BaseModel):
    habrulesid = models.IntegerField(primary_key=True)
    kii = models.ForeignKey(KII, on_delete=models.PROTECT)
    habnamel = models.CharField(max_length=255, default=str(NODATA[0]))
    habname = models.CharField(max_length=255, default=str(NODATA[0]))
    habrule = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    habspecificrulel = models.TextField(default=str(NODATA[0]))
    habspecificrule = models.TextField(default=str(NODATA[0]))

    def __str__(self):
        return self.habname


class Right(BaseModel):
    KII_GOVT_SUPPORT_CHOICES = [
        (1, "Sangat menentang / Strongly oppose"),
        (2, "Menentang / Oppose"),
        (3, "Tidak menantang maupan mendukung / Neither oppose nor support"),
        (4, "Mendukung / Support"),
        (5, "Sangat mendukung / Strongly support"),
    ] + SKIP_CODES
    KII_RULE_INCLUDED_CHOICES = [
        (1, "Tidak dimasukkan / Not included"),
        (2, "Dimasukkan sebagian / Partially included"),
        (3, "Dimasukkan semua / Fully included"),
    ] + SKIP_CODES
    rightsid = models.IntegerField(primary_key=True)
    kii = models.ForeignKey(KII, on_delete=models.PROTECT)
    usernamel = models.CharField(max_length=255, default=str(NODATA[0]))
    username = models.CharField(max_length=255, default=str(NODATA[0]))
    userrule = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    userspecrulel = models.CharField(max_length=255, default=str(NODATA[0]))
    userspecrule = models.CharField(max_length=255, default=str(NODATA[0]))
    govtsupport = models.PositiveSmallIntegerField(
        choices=KII_GOVT_SUPPORT_CHOICES, default=NODATA[0]
    )
    userrulesinc = models.PositiveSmallIntegerField(
        choices=KII_RULE_INCLUDED_CHOICES, default=NODATA[0]
    )
    notes = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.userrule


class SpeciesRule(BaseModel):
    sppruleid = models.IntegerField(primary_key=True)
    kii = models.ForeignKey(KII, on_delete=models.PROTECT)
    speciescommonl = models.CharField(max_length=255, default=str(NODATA[0]))
    speciescommon = models.CharField(max_length=255, default=str(NODATA[0]))
    family = models.CharField(max_length=255, default=str(NODATA[0]))
    genus = models.CharField(max_length=255, default=str(NODATA[0]))
    species = models.CharField(max_length=255, default=str(NODATA[0]))
    spprule = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    sppspecificrulel = models.TextField(default=str(NODATA[0]))
    sppspecificrule = models.TextField(default=str(NODATA[0]))

    def __str__(self):
        return self.spprule


class Zone(BaseModel):
    zoneid = models.IntegerField(primary_key=True)
    kii = models.ForeignKey(KII, on_delete=models.PROTECT)
    zonetypel = models.CharField(max_length=255, default=str(NODATA[0]))
    zonetype = models.CharField(max_length=255, default=str(NODATA[0]))
    zonequantity = models.PositiveSmallIntegerField(default=NODATA[0])
    zoneorg = models.CharField(max_length=255, default=str(NODATA[0]))
    zonecoord = models.PositiveSmallIntegerField(
        choices=KII_FREQ_CHOICES, default=NODATA[0]
    )
    notes = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.zonetype
