from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from .base import (
    NODATA,
    YES_NO_CHOICES,
    MAX_YEAR,
    YEAR_CHOICES,
    MONITORING_FREQUENCY_CHOICES,
    MinValueBCValidator,
    MaxValueBCValidator,
    BaseModel,
    MonitoringStaff,
    Settlement,
)


class FGDSurveyVersion(BaseModel):
    version = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.version


class FGD(BaseModel):
    fgdid = models.IntegerField(primary_key=True)
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT)
    fgdcode = models.PositiveSmallIntegerField(default=NODATA[0])
    facilitator = models.ForeignKey(
        MonitoringStaff, on_delete=models.PROTECT, related_name="fgd_staff_facilitator"
    )
    notetaker = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.PROTECT,
        default=NODATA[0],
        related_name="fgd_staff_notetaker",
    )
    fgdate = models.DateField(null=True, blank=True)
    yearmonitoring = models.PositiveSmallIntegerField(
        choices=YEAR_CHOICES,
        validators=[MinValueBCValidator(2000), MaxValueBCValidator(MAX_YEAR)],
        default=NODATA[0],
    )
    starttime = models.TimeField()
    endtime = models.TimeField()
    maleparticipants = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(100)], default=NODATA[0]
    )
    femaleparticipants = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(100)], default=NODATA[0]
    )
    fgdversion = models.ForeignKey(
        FGDSurveyVersion, on_delete=models.PROTECT, default=NODATA[0]
    )
    fgroundname = models.CharField(max_length=255, default=str(NODATA[0]))
    fgroundboat = models.CharField(max_length=255, default=str(NODATA[0]))
    fgroundtime = models.CharField(max_length=255, default=str(NODATA[0]))
    fgrounddist = models.CharField(max_length=255, default=str(NODATA[0]))
    fgroundsize = models.CharField(max_length=255, default=str(NODATA[0]))
    mpaname = models.CharField(max_length=255, default=str(NODATA[0]))
    mpaboat = models.CharField(max_length=255, default=str(NODATA[0]))
    mpatime = models.CharField(max_length=255, default=str(NODATA[0]))
    mpadist = models.CharField(max_length=255, default=str(NODATA[0]))
    mpasize = models.CharField(max_length=255, default=str(NODATA[0]))
    ntname = models.CharField(max_length=255, default=str(NODATA[0]))
    ntboat = models.CharField(max_length=255, default=str(NODATA[0]))
    nttime = models.CharField(max_length=255, default=str(NODATA[0]))
    ntdist = models.CharField(max_length=255, default=str(NODATA[0]))
    ntsize = models.CharField(max_length=255, default=str(NODATA[0]))
    mpahistl = models.TextField(default=str(NODATA[0]))
    mpahist = models.TextField(default=str(NODATA[0]))
    extbnd = models.PositiveSmallIntegerField(
        validators=[MinValueBCValidator(0), MaxValueBCValidator(100)], default=NODATA[0]
    )
    intbnd = models.PositiveSmallIntegerField(
        validators=[MinValueBCValidator(0), MaxValueBCValidator(100)], default=NODATA[0]
    )
    bndlandmarks = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndmarkers = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndsigns = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndgovnotice = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndwoutreach = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndaoutreach = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndvoutreach = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndword = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndotheroutreach = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    bndotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    bndotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    penaltyverbal = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(999)], default=NODATA[0]
    )
    penaltywritten = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyequipment = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyfines = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyprison = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyother = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    penaltyotherspecifyl = models.CharField(max_length=255, default=str(NODATA[0]))
    penaltyotherspecify = models.CharField(max_length=255, default=str(NODATA[0]))
    npenalty = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(7)], default=NODATA[0]
    )
    verbalsanction = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    physicalsanction = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    monetarysanction = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    conflictl = models.TextField(default=str(NODATA[0]))
    conflict = models.TextField(default=str(NODATA[0]))
    conflictusertime = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=NODATA[0],
        validators=[MinValueValidator(0)],
    )
    conflictofficialtime = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=NODATA[0],
        validators=[MinValueValidator(0)],
    )
    conflictusercost = models.PositiveIntegerField(
        validators=[MaxValueBCValidator(1000000000)], default=NODATA[0]
    )
    conflictofficialcost = models.PositiveIntegerField(
        validators=[MaxValueBCValidator(1000000000)], default=NODATA[0]
    )
    conflictuserdist = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=NODATA[0],
        validators=[MinValueValidator(0)],
    )
    conflictofficialdist = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        default=NODATA[0],
        validators=[MinValueValidator(0)],
    )
    otherinfol = models.TextField(default=str(NODATA[0]))
    otherinfo = models.TextField(default=str(NODATA[0]))
    otherpeoplel = models.TextField(default=str(NODATA[0]))
    otherpeople = models.TextField(default=str(NODATA[0]))
    othersourcesl = models.TextField(default=str(NODATA[0]))
    othersources = models.TextField(default=str(NODATA[0]))
    traditionalgovernancel = models.TextField(default=str(NODATA[0]))
    traditionalgovernance = models.TextField(default=str(NODATA[0]))
    conflictn = models.CharField(max_length=255, default=str(NODATA[0]))
    congroup = models.CharField(max_length=255, default=str(NODATA[0]))
    conbtwgroups = models.CharField(max_length=255, default=str(NODATA[0]))
    conbtwgroupngov = models.CharField(max_length=255, default=str(NODATA[0]))
    congov = models.CharField(max_length=255, default=str(NODATA[0]))
    contypemarine = models.CharField(max_length=255, default=str(NODATA[0]))
    contypegov = models.CharField(max_length=255, default=str(NODATA[0]))
    contypeusers = models.CharField(max_length=255, default=str(NODATA[0]))
    contyperec = models.CharField(max_length=255, default=str(NODATA[0]))
    contypeother = models.CharField(max_length=255, default=str(NODATA[0]))
    contypeotherspecifyl = models.TextField(default=str(NODATA[0]))
    contypeotherspecify = models.TextField(default=str(NODATA[0]))
    dataentryid = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fgd_staff_data_entry",
    )
    datacheckid = models.ForeignKey(
        MonitoringStaff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fgd_staff_data_check",
    )
    notesl = models.TextField(default=str(NODATA[0]))
    notes = models.TextField(default=str(NODATA[0]))
    qaqcnotes = models.TextField(default=str(NODATA[0]))

    @property
    def mpa(self):
        return self.settlement.mpa.mpaid

    class Meta:
        verbose_name = _("FGD")
        verbose_name_plural = _("FGDs")

    def __str__(self):
        return str(self.pk)


class Users(BaseModel):
    userid = models.IntegerField(primary_key=True)
    fgd = models.ForeignKey(FGD, on_delete=models.PROTECT)
    usercode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    usernamel = models.CharField(max_length=255, default=str(NODATA[0]))
    username = models.CharField(max_length=255, default=str(NODATA[0]))
    userextbnd = models.ForeignKey(
        "LkpNoneToAllScale",
        related_name="nonetoall_externalboundary",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    userintbnd = models.ForeignKey(
        "LkpNoneToAllScale",
        related_name="nonetoall_internalboundary",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    participateestablish = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participateboundaries = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participateadmin = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participaterules = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    monitoreco = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    monitorsoc = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    monitorcompliance = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    enforcefreq = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    contributionrank = models.PositiveSmallIntegerField(
        validators=[MinValueBCValidator(1), MaxValueBCValidator(25)], default=NODATA[0]
    )
    benefitrank = models.PositiveSmallIntegerField(
        validators=[MinValueBCValidator(1), MaxValueBCValidator(25)], default=NODATA[0]
    )
    monitorcovidl = models.TextField(default=str(NODATA[0]))
    monitorcovid = models.TextField(default=str(NODATA[0]))
    covidassistancel = models.TextField(default=str(NODATA[0]))
    covidassistance = models.TextField(default=str(NODATA[0]))
    conservationimpactcovidl = models.TextField(default=str(NODATA[0]))
    conservationimpactcovid = models.TextField(default=str(NODATA[0]))

    def __str__(self):
        return self.username


class Habitat(BaseModel):
    habitatid = models.IntegerField(primary_key=True)
    fgd = models.ForeignKey(FGD, on_delete=models.PROTECT)
    habitatcode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    habitattypel = models.CharField(max_length=255, default=str(NODATA[0]))
    habitattype = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.habitatcode


class Rule(BaseModel):
    ruleid = models.IntegerField(primary_key=True)
    fgd = models.ForeignKey(FGD, on_delete=models.SET_NULL, null=True, blank=True)
    rulecode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    rulel = models.TextField(default=str(NODATA[0]))
    rule = models.TextField(default=str(NODATA[0]))

    def __str__(self):
        return self.rulecode


class Species(BaseModel):
    speciesid = models.IntegerField(primary_key=True)
    fgd = models.ForeignKey(FGD, on_delete=models.PROTECT, null=True, blank=True)
    speciescommonl = models.CharField(max_length=255, default=str(NODATA[0]))
    speciescommon = models.CharField(max_length=255, default=str(NODATA[0]))
    family = models.CharField(max_length=255, default=str(NODATA[0]))
    genus = models.CharField(max_length=255, default=str(NODATA[0]))
    species = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.species

    class Meta:
        verbose_name_plural = "species"


class Stakeholder(BaseModel):
    stakeholderid = models.IntegerField(primary_key=True)
    fgd = models.ForeignKey(FGD, on_delete=models.PROTECT, null=True, blank=True)
    stakeholdernamel = models.CharField(max_length=255, default=str(NODATA[0]))
    stakeholdername = models.CharField(max_length=255, default=str(NODATA[0]))
    participateestablish = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participateboundaries = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participateadmin = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    participaterules = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    monitoreco = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    monitorsoc = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    monitorcompliance = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )
    enforcefreq = models.PositiveSmallIntegerField(
        choices=MONITORING_FREQUENCY_CHOICES, default=NODATA[0]
    )

    def __str__(self):
        return self.stakeholderid
