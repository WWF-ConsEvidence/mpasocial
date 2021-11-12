from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .base import (
    NODATA,
    SKIP_CODES,
    YES_NO_CHOICES,
    GENDER_CHOICES,
    ORGANIZATION_POSITION_CHOICES,
    MAX_YEAR,
    YEAR_CHOICES,
    MinValueBCValidator,
    MaxValueBCValidator,
    BaseModel,
    BaseLookupModel,
    Settlement,
)


class HouseholdSurveyVersion(BaseModel):
    version = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.version


class LkpAssetAssistance(BaseLookupModel):
    class Meta:
        ordering = ("code",)


class LkpAssetObtain(BaseLookupModel):
    class Meta:
        ordering = ("code",)


class LkpFreqFishTime(BaseLookupModel):
    class Meta:
        ordering = ("code",)

    def __str__(self):
        return "{} [{}]".format(self.bahasaindonesia, self.english)


class LkpFishTechCategory(BaseLookupModel):
    class Meta:
        ordering = ("code",)
        verbose_name_plural = "lkp fish tech categories"

    def __str__(self):
        return str(self.code)


class LkpFishTechnique(BaseLookupModel):
    consolidatedfishtechcategory = models.ForeignKey(
        LkpFishTechCategory, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ("code",)

    def __str__(self):
        return "{} [{}]".format(self.bahasaindonesia, self.english)


class LkpLivelihood(BaseLookupModel):
    class Meta:
        ordering = ("code",)

    def __str__(self):
        return "{} [{}]".format(self.bahasaindonesia, self.english)


class Household(BaseModel):
    ATT_SCALE_CHOICES = [
        (1, "Apakah anda sangat tidak setuju / Strongly disagree"),
        (2, "Tidak setuju / Disagree"),
        (3, "Netral / Neither agree nor disagree"),
        (4, "Setuju atau / Agree"),
        (5, "Dangat setuju dengan pernyataan ini / Strongly agree"),
    ] + SKIP_CODES
    COOKING_FUEL_CHOICES = [
        (1, "Listrik/Gas / Electricity or gas"),
        (2, "Minyak/Minyak Tanah / Oil"),
        (3, "Kayu / Wood"),
        (4, "Arang / Charcoal"),
        (5, "Kayu ranting atau serpihan kayu / Small sticks/scrap wood"),
        (6, " Serasah, daun, biogas / Weeds, leaves, dung"),
    ] + SKIP_CODES
    ECONOMIC_STATUS_TREND_CHOICES = [
        (1, "Mejadi sangat buruk / Much worse"),
        (2, "Menjadi sedikit lebih buruk / Slightly worse"),
        (3, "Tidak berubah / No change"),
        (4, "Menjadi sedikit lebih baik / Slightly better"),
        (5, "Menjadi sangat baik / Much better"),
    ] + SKIP_CODES
    FS_CHOICES = [
        (1, "Sering / Often true"),
        (2, "Kadang-kadang / Sometimes true"),
        (3, "Tidak pernah / Never true"),
    ] + SKIP_CODES
    FS_FREQ_CHOICES = [
        (1, "Hampir setiap bulan / Almost every month"),
        (
            2,
            "Beberapa bulan tetapi tidak setiap bulan / Some months but not every month",
        ),
        (3, "Hanya satu atau dua bulan / Only one or two months a year"),
    ] + SKIP_CODES
    RELIGION_CHOICES = [
        (1, "Kristen / Christian"),
        (2, "Islam / Muslim"),
        (3, "Hindu / Hindu"),
        (4, "Budha / Buddhist"),
        (5, "Yahudi / Jewish"),
        (6, "Kepercataan Tradisional / Traditional Beliefs"),
        (7, "Atheis / Atheist"),
        (8, "Katolik / Catholic"),
    ] + SKIP_CODES
    SOCIAL_CONFLICT_CHOICES = [
        (1, "Sangat meningkat / Greatly Increased"),
        (2, "Meningkat / Increased"),
        (3, "Tidak ada perubahan / Neither increased nor decreased"),
        (4, "Menurun / Decreased"),
        (5, "Sangat menurum / Greatly decreased"),
    ] + SKIP_CODES
    CATCH_UNIT_CHOICES = [
        (1, "Tali / Line"),
        (2, "Ember / Bucket"),
        (3, "Wayah / Wayah (no English translation available)"),
        (4, "Ekor / Tail"),
        (5, "Loyang / Tray"),
    ] + SKIP_CODES

    householdid = models.IntegerField(primary_key=True)
    settlement = models.ForeignKey(Settlement, on_delete=models.PROTECT)
    kkcode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    primaryinterviewer = models.ForeignKey(
        "MonitoringStaff",
        on_delete=models.PROTECT,
        related_name="household_primaryinterviewer",
    )
    secondaryinterviewer = models.ForeignKey(
        "MonitoringStaff",
        on_delete=models.PROTECT,
        related_name="household_secondaryinterviewer",
        default=NODATA[0],
    )
    fieldcoordinator = models.ForeignKey(
        "MonitoringStaff",
        on_delete=models.PROTECT,
        related_name="household_fieldcoordinator",
    )
    yearmonitoring = models.PositiveSmallIntegerField(
        choices=YEAR_CHOICES,
        validators=[MinValueBCValidator(2000), MaxValueBCValidator(MAX_YEAR)],
        default=NODATA[0],
    )
    interviewdate = models.DateField(blank=True, null=True)
    interviewstart = models.TimeField(blank=True, null=True)
    interviewend = models.TimeField(blank=True, null=True)
    interviewlength = models.TimeField(blank=True, null=True)
    surveyversionnumber = models.ForeignKey(
        HouseholdSurveyVersion, on_delete=models.PROTECT
    )
    usualfish = models.CharField(max_length=255, default=str(NODATA[0]))
    householdsize = models.PositiveSmallIntegerField(default=NODATA[0])
    yearsresident = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(150)], default=NODATA[0]
    )
    primarymarketname = models.CharField(max_length=255, default=str(NODATA[0]))
    secondarymarketname = models.CharField(max_length=255, default=str(NODATA[0]))
    timemarket = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(0)],
        default=NODATA[0],
    )
    timesecondarymarket = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(0)],
        default=NODATA[0],
    )
    paternalethnicity = models.CharField(max_length=255, default=str(NODATA[0]))
    maternalethnicity = models.CharField(max_length=255, default=str(NODATA[0]))
    religion = models.PositiveSmallIntegerField(
        choices=RELIGION_CHOICES, default=NODATA[0]
    )
    primarylivelihood = models.ForeignKey(
        "LkpLivelihood",
        related_name="livelihood_primarylivelihood",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    primarylivelihoodyear = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    secondarylivelihood = models.ForeignKey(
        "LkpLivelihood",
        related_name="livelihood_secondarylivelihood",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    secondarylivelihoodyear = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    tertiarylivelihood = models.ForeignKey(
        "LkpLivelihood",
        related_name="livelihood_tertiarylivelihood",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    tertiarylivelihoodyear = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    freqfishtime = models.ForeignKey(
        "LkpFreqFishTime",
        related_name="freqfishtime_freqfish",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    freqsalefish = models.ForeignKey(
        "LkpFreqFishTime",
        related_name="freqfishtime_freqsalefish",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    percentincomefish = models.ForeignKey(
        "LkpNoneToAllScale",
        related_name="nonetoall_percentincomefish",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    freqeatfish = models.ForeignKey(
        "LkpFreqFishTime",
        related_name="freqfishtime_freqeatfish",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    percentproteinfish = models.ForeignKey(
        "LkpNoneToAllScale",
        related_name="nonetoall_percentproteinfish",
        on_delete=models.PROTECT,
        default=NODATA[0],
    )
    majorfishtechnique = models.ForeignKey(
        "LkpFishTechCategory", on_delete=models.PROTECT, default=NODATA[0]
    )
    primaryfishtechnique = models.ForeignKey(
        "LkpFishTechnique",
        on_delete=models.PROTECT,
        default=NODATA[0],
        related_name="primaryfishtechnique_households",
    )
    secondaryfishtechnique = models.ForeignKey(
        "LkpFishTechnique",
        on_delete=models.PROTECT,
        default=NODATA[0],
        related_name="secondaryfishtechnique_households",
    )
    tertiaryfishtechnique = models.ForeignKey(
        "LkpFishTechnique",
        on_delete=models.PROTECT,
        default=NODATA[0],
        related_name="tertiaryfishtechnique_households",
    )
    lessproductivedaysfishing = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(365)], default=NODATA[0]
    )
    poorcatch = models.PositiveIntegerField(default=NODATA[0])
    poorcatchunits = models.CharField(max_length=255, default=str(NODATA[0]))
    poorcatchunitscategory = models.PositiveSmallIntegerField(
        choices=CATCH_UNIT_CHOICES, default=NODATA[0]
    )
    poorfishincome = models.PositiveIntegerField(default=NODATA[0])
    poorfishincomeunits = models.CharField(max_length=255, default=str(NODATA[0]))
    moreproductivedaysfishing = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(365)], default=NODATA[0]
    )
    goodcatch = models.PositiveIntegerField(default=NODATA[0])
    goodcatchunits = models.CharField(max_length=255, default=str(NODATA[0]))
    goodcatchunitscategory = models.PositiveSmallIntegerField(
        choices=CATCH_UNIT_CHOICES, default=NODATA[0]
    )
    goodfishincome = models.PositiveIntegerField(default=NODATA[0])
    goodfishincomeunits = models.CharField(max_length=255, default=str(NODATA[0]))
    economicstatustrend = models.PositiveSmallIntegerField(
        choices=ECONOMIC_STATUS_TREND_CHOICES, default=NODATA[0]
    )
    economicstatusreasonl = models.TextField(default=str(NODATA[0]))
    economicstatusreason = models.TextField(default=str(NODATA[0]))
    economicadjustreasonl = models.TextField(default=str(NODATA[0]))
    economicadjustreason = models.TextField(default=str(NODATA[0]))
    assetcar = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(30)], default=NODATA[0]
    )
    assetcarobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcarobtains",
    )
    assetcaryear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetcarassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcarassistance",
    )
    assetcarassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assettruck = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assettruckobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assettruckobtains",
    )
    assettruckyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assettruckassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assettruckassistance",
    )
    assettruckassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assetcartruck = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetbicycle = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetbicycleobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetbicycleobtains",
    )
    assetbicycleyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetbicycleassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetbicycleassistance",
    )
    assetbicycleassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetmotorcycle = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetmotorcycleobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetmotorcycleobtains",
    )
    assetmotorcycleyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetmotorcycleassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetmotorcycleassistance",
    )
    assetmotorcycleassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetboatnomotor = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetboatnomotorobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatnomotorobtains",
    )
    assetboatnomotoryear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetboatnomotorassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatnomotorassistance",
    )
    assetboatnomotorassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetboatoutboard = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetboatoutboardobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatoutboardobtains",
    )
    assetboatoutboardyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetboatoutboardassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatoutboardassistance",
    )
    assetboatoutboardassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetboatinboard = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetboatinboardobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatinboardobtains",
    )
    assetboatinboardyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetboatinboardassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetboatinboardassistance",
    )
    assetboatinboardassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetlandlinephone = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetlandlinephoneobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetlandlinephoneobtains",
    )
    assetlandlinephoneyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetlandlinephoneassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetlandlinephoneassistance",
    )
    assetlandlinephoneassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetcellphone = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetcellphoneobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcellphoneobtains",
    )
    assetcellphoneyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetcellphoneassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcellphoneassistance",
    )
    assetcellphoneassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetphonecombined = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assettv = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assettvobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assettvobtains",
    )
    assettvyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assettvassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assettvassistance",
    )
    assettvassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assetradio = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetradioobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetradioobtains",
    )
    assetradioyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetradioassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetradioassistance",
    )
    assetradioassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assetstereo = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetstereoobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetstereoobtains",
    )
    assetstereoyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetstereoassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetstereoassistance",
    )
    assetstereoassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetcd = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetcdobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcdobtains",
    )
    assetcdyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetcdassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetcdassistance",
    )
    assetcdassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assetdvd = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetdvdobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetdvdobtains",
    )
    assetdvdyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetdvdassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetdvdassistance",
    )
    assetdvdassistanceother = models.CharField(max_length=255, default=str(NODATA[0]))
    assetentertain = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetsatellite = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetsatelliteobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetsatelliteobtains",
    )
    assetsatelliteyear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetsatelliteassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetsatelliteassistance",
    )
    assetsatelliteassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    assetgenerator = models.PositiveSmallIntegerField(
        validators=[MaxValueBCValidator(50)], default=NODATA[0]
    )
    assetgeneratorobtain = models.ForeignKey(
        "LkpAssetObtain",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetgeneratorobtains",
    )
    assetgeneratoryear = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(1900),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )
    assetgeneratorassistance = models.ForeignKey(
        "LkpAssetAssistance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_assetgeneratorassistance",
    )
    assetgeneratorassistanceother = models.CharField(
        max_length=255, default=str(NODATA[0])
    )
    cookingfuel = models.PositiveSmallIntegerField(
        choices=COOKING_FUEL_CHOICES, default=NODATA[0]
    )
    householddeath = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    householdbirth = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsnotenough = models.PositiveSmallIntegerField(
        choices=FS_CHOICES, default=NODATA[0]
    )
    fsdidnotlast = models.PositiveSmallIntegerField(
        choices=FS_CHOICES, default=NODATA[0]
    )

    fsbalanceddiet = models.PositiveSmallIntegerField(
        choices=FS_CHOICES, default=NODATA[0]
    )

    fsadultskip = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsfreqadultskip = models.PositiveSmallIntegerField(
        choices=FS_FREQ_CHOICES, default=NODATA[0]
    )
    fseatless = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fshungry = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fschildportion = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fslowcostfood = models.PositiveSmallIntegerField(
        choices=FS_CHOICES, default=NODATA[0]
    )
    fschildskip = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsfreqchildskip = models.PositiveSmallIntegerField(
        choices=FS_FREQ_CHOICES, default=NODATA[0]
    )
    fsnomealchild = models.PositiveSmallIntegerField(
        choices=FS_CHOICES, default=NODATA[0]
    )
    rightsaccess = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    rightsharvest = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    rightsmanage = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    rightsexclude = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    rightstransfer = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    socialconflict = models.PositiveSmallIntegerField(
        choices=SOCIAL_CONFLICT_CHOICES, default=NODATA[0]
    )
    marinegroup = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    numbermarinegroup = models.PositiveSmallIntegerField(default=NODATA[0])
    othergroup = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    numberothergroup = models.PositiveSmallIntegerField(default=NODATA[0])
    votedistrict = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    votenational = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    numlocalthreat = models.PositiveSmallIntegerField(default=NODATA[0])
    numglobalthreat = models.PositiveSmallIntegerField(default=NODATA[0])
    numlocalaction = models.PositiveSmallIntegerField(default=NODATA[0])
    numglobalaction = models.PositiveSmallIntegerField(default=NODATA[0])
    placehappy = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    placefavourite = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    placemiss = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    placebest = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    placefishhere = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    placebemyself = models.PositiveSmallIntegerField(
        choices=ATT_SCALE_CHOICES, default=NODATA[0]
    )
    primarylivelihoodcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    secondarylivelihoodcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    tertiarylivelihoodcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    freqfishtimecovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    freqsalefishcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    percentincomefishcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    freqeatfishcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    percentproteinfishcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    majorfishtechniquecovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    poorfishincomecovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    goodfishincomecovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsnotenoughcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsdidnotlastcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsbalanceddietcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fseatlesscovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fshungrycovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fschildportioncovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fslowcostfoodcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsfreqchildskipcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    fsnomealchildcovid = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    marinegroupcovid = models.TextField(default=str(NODATA[0]))
    othergroupcovid = models.TextField(default=str(NODATA[0]))

    anyotherinfo = models.TextField(default=str(NODATA[0]))
    willingparticipant = models.TextField(default=str(NODATA[0]))
    notes = models.TextField(default=str(NODATA[0]))
    dataentrycomplete = models.BooleanField(blank=True, null=True)
    datacheckcomplete = models.BooleanField(blank=True, null=True)
    dataentryid = models.ForeignKey(
        "MonitoringStaff",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="household_dataentrystaff",
    )
    datacheckid = models.ForeignKey(
        "MonitoringStaff",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="household_datacheckstaff",
    )
    worstdaycatch = models.CharField(max_length=255, default=str(NODATA[0]))
    worstdaycatchunits = models.CharField(max_length=255, default=str(NODATA[0]))
    bestdaycatch = models.CharField(max_length=255, default=str(NODATA[0]))
    bestdaycatchunits = models.CharField(max_length=255, default=str(NODATA[0]))
    averageincome = models.CharField(max_length=255, default=str(NODATA[0]))
    averageincomeunits = models.CharField(max_length=255, default=str(NODATA[0]))
    worstincome = models.CharField(max_length=255, default=str(NODATA[0]))
    worstincomeunits = models.CharField(max_length=255, default=str(NODATA[0]))
    bestincome = models.CharField(max_length=255, default=str(NODATA[0]))
    bestincomeunits = models.CharField(max_length=255, default=str(NODATA[0]))
    entrycomputeridentifier = models.CharField(max_length=255, default=str(NODATA[0]))
    entryhouseholdid = models.IntegerField(blank=True, null=True)
    pilotreferencecode = models.CharField(max_length=255, default=str(NODATA[0]))
    baseline_t2_pairs = models.FloatField(blank=True, null=True)

    @property
    def mpa(self):
        return self.settlement.mpa.mpaid

    def __str__(self):
        return str(self.householdid) or ""


class Birth(BaseModel):
    birthid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    infantsurvived = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    dateofdeath = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(2000),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )

    def __str__(self):
        return str(self.pk)


class Death(BaseModel):
    deathid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    gender = models.IntegerField(choices=GENDER_CHOICES, default=NODATA[0])
    ageatdeath = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=NODATA[0],
        validators=[MinValueBCValidator(0), MaxValueBCValidator(150)],
    )
    datedeath = models.PositiveSmallIntegerField(
        validators=[
            MinValueBCValidator(2000),
            MaxValueBCValidator(timezone.now().year),
        ],
        default=NODATA[0],
    )

    def __str__(self):
        return self.pk


class Demographic(BaseModel):
    EDUCATION_LEVEL_CHOICES = [
        (0, "Tidak Ada Pendidikan Formal / No Formal Education"),
        (1, "Taman Kanak-kanak / Pre-School"),
        (2, "Sekolah Dasar (SD) / Primary School"),
        (3, "Sekolah Menengah Pertama (SMP) / Middle  School "),
        (
            4,
            "Sekolah Menengah Atas (SMA) dan Sekolah Menengah Kejuruan (SMK)/ Secondary School",
        ),
        (
            5,
            " Ahli Madya Diploma 3 dan lebih tinggi  (S1, S2, S3) / Post Secondary School",
        ),
    ] + SKIP_CODES
    RELATIONSHIP_CHOICES = [
        (0, "Kepala keluarga"),
        (1, "Pasangan (suami/istri) / Spouse"),
        (2, "Anak / Child"),
        (3, "Ibu/Ayah mertua / Father/Mother in law"),
        (4, "Cucu / Grandchild"),
        (5, "Orang tua / Parent"),
        (6, "Anak mantu or Anak menantu  / Child in law"),
        (7, "Saudara laki-laki/perempuan / Sibling"),
        (8, "Ipar / Sibling in law"),
        (9, "Paman/Bibi (Om/Tante) / Uncle or Aunt"),
        (10, "Keponakan / Nephew or Neice"),
        (11, "Anak tiri or Anak angkat / Foster child"),
        (12, "Keluarga lainnya / Other family member"),
        (13, "Tidak ada hubungan kekerabatan / Not related to family"),
    ] + SKIP_CODES
    demographicid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    demographiccode = models.PositiveSmallIntegerField(
        default=NODATA[0], validators=[MinValueBCValidator(1), MaxValueBCValidator(999)]
    )
    relationhhh = models.IntegerField(choices=RELATIONSHIP_CHOICES, default=NODATA[0])
    individualage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=NODATA[0],
        validators=[MinValueBCValidator(0), MaxValueBCValidator(150)],
    )
    individualgender = models.IntegerField(choices=GENDER_CHOICES, default=NODATA[0])
    individualeducation = models.CharField(max_length=255, default=str(NODATA[0]))
    individualedlevel = models.IntegerField(
        choices=EDUCATION_LEVEL_CHOICES, default=NODATA[0]
    )
    individualenrolled = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    householdhead = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    individualunwell = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    individualdaysunwell = models.PositiveIntegerField(
        validators=[MaxValueBCValidator(31)], default=NODATA[0]
    )
    individuallostdays = models.PositiveIntegerField(
        validators=[MaxValueBCValidator(31)], default=NODATA[0]
    )

    def __str__(self):
        return str(self.demographiccode)


class GlobalStep(BaseModel):
    globalstepsid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    globalmarinesteps = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.globalmarinesteps


class GlobalThreat(BaseModel):
    globalthreatid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    globalmarinethreat = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.globalmarinethreat


class LocalStep(BaseModel):
    localstepsid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    localsteps = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.localsteps


class LocalThreat(BaseModel):
    localthreatid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    localmarinethreat = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.localmarinethreat


class NonMarineOrganizationMembership(BaseModel):
    nmorganizationid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    name = models.CharField(max_length=255, default=str(NODATA[0]))
    position = models.IntegerField(
        choices=ORGANIZATION_POSITION_CHOICES, default=NODATA[0]
    )
    meeting = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    days = models.PositiveIntegerField(
        default=NODATA[0], validators=[MaxValueBCValidator(365)]
    )
    contribution = models.IntegerField(default=NODATA[0])
    contributionunits = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.pk


class MarineOrganizationMembership(BaseModel):
    morganizationid = models.IntegerField(primary_key=True)
    household = models.ForeignKey(Household, on_delete=models.PROTECT)
    entryhouseholdid = models.BigIntegerField(default=NODATA[0])
    name = models.CharField(max_length=255, default=str(NODATA[0]))
    position = models.IntegerField(
        choices=ORGANIZATION_POSITION_CHOICES, default=NODATA[0]
    )
    meeting = models.PositiveSmallIntegerField(
        choices=YES_NO_CHOICES, default=NODATA[0]
    )
    days = models.PositiveIntegerField(
        default=NODATA[0], validators=[MaxValueBCValidator(365)]
    )
    contribution = models.IntegerField(default=NODATA[0])
    contributionunits = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.pk
