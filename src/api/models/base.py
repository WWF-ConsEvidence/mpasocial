from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db.models.fields import PolygonField, MultiPolygonField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


NODATA = (995, "Tidak Ada data / No data")
SKIP_CODES = [
    (
        993,
        "Pertanyaan tidak diminta (tidak ada skip logic) / Question not asked (no skip logic)",
    ),
    (994, "SKIP / Skipped based on survey skip logic"),
    NODATA,
    (996, "Lainnya / Other"),
    (997, "Tidak tahu / Do not know"),
    (998, "Tidak sesuai / Not applicable"),
    (999, "Menolak / Refused"),
]
SKIP_CODE_KEYS = [code[0] for code in SKIP_CODES]

MAX_YEAR = 2050
YEAR_CHOICES = [y for y in zip(*[range(2000, MAX_YEAR + 1)] * 2)] + SKIP_CODES
YES_NO_CHOICES = [(0, "Tidak / No"), (1, "Ya / Yes")] + SKIP_CODES

GENDER_CHOICES = [(1, "Laki-Laki / Male"), (2, " Perempuan / Female")] + SKIP_CODES
KII_FREQ_CHOICES = [
    (1, "Tidak pernah / Never"),
    (2, "Hampir tidak pernah / Rarely"),
    (3, "Kadang-kadang / Sometimes"),
    (4, "Biasanya / Usually"),
    (5, "Selalu / Always"),
] + SKIP_CODES
MONITORING_FREQUENCY_CHOICES = [
    (1, "Kurang dari satu kali per tahun / Less than one time per year"),
    (2, "Beberapa kali per tahun / A few times per year"),
    (3, "Beberapa kali per bulan / A few times per month"),
    (4, "Berberapa kali per minggu / A few times per week"),
    (5, "Lebih dari satu kali sehari / More than once per day"),
] + SKIP_CODES
ORGANIZATION_POSITION_CHOICES = [
    (1, "Anggota / Member"),
    (2, " Pengurus / Official"),
] + SKIP_CODES


class MinValueBCValidator(MinValueValidator):
    def compare(self, a, b):
        return a < b and a not in SKIP_CODE_KEYS


class MaxValueBCValidator(MaxValueValidator):
    def compare(self, a, b):
        return a > b and a not in SKIP_CODE_KEYS


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))

    class Meta:
        abstract = True


class BaseLookupModel(BaseModel):
    code = models.IntegerField(primary_key=True)
    bahasaindonesia = models.CharField(max_length=255, blank=True)
    english = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class BaseChoiceModel(BaseModel):
    @property
    def choice(self):
        ret = {"id": self.pk, "name": self.__str__(), "updated_on": self.updated_on}
        if hasattr(self, "val"):
            ret["val"] = self.val
        return ret

    class Meta:
        abstract = True


class AreaMixin(models.Model):
    def get_polygon(self):
        for f in self._meta.get_fields():
            if isinstance(f, PolygonField) or isinstance(f, MultiPolygonField):
                return getattr(self, f.attname)  # return poly object, not field
        return None

    @property
    def area(self):
        field = self.get_polygon()
        if field is None:
            return None
        if hasattr(self, "_area"):
            return self._area
        # using a world equal area projection to do the areal measurement; there may be a better one
        # https://epsg.io/3410
        # Thought geography=True would make this unnecessary
        self._area = round(field.transform(3410, clone=True).area / 10000, 3)
        return self._area

    area.fget.short_description = _("area (ha)")

    class Meta:
        abstract = True


class Country(BaseChoiceModel):
    iso = models.CharField(max_length=5)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "countries"
        ordering = ("name",)

    def __unicode__(self):
        return _("%s") % self.name

    def __str__(self):
        return self.name


class UserProfile(BaseModel):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    mpa_interviewyears = models.ManyToManyField(
        "MPAInterviewYear", blank=True, verbose_name="MPA interview years"
    )

    def __str__(self):
        return f"{self.user.username} profile"


class MPANetwork(BaseLookupModel):
    class Meta:
        ordering = ("code",)


class Seascape(BaseLookupModel):
    class Meta:
        ordering = ("code",)


class MPA(BaseModel, AreaMixin):
    mpaid = models.IntegerField(primary_key=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    mpaname = models.CharField(max_length=255)
    mpanetwork = models.ForeignKey(
        MPANetwork, on_delete=models.SET_NULL, null=True, blank=True
    )
    seascape = models.ForeignKey(
        Seascape, on_delete=models.SET_NULL, null=True, blank=True
    )
    wdpaid = models.IntegerField(null=True, blank=True)
    estyear = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(timezone.now().year)],
        verbose_name=_("year established"),
        null=True,
        blank=True,
    )
    notes = models.TextField(default=str(NODATA[0]))
    boundary = models.MultiPolygonField(geography=True, null=True, blank=True)
    size = models.IntegerField(verbose_name=_("Size (km2)"), null=True, blank=True)

    class Meta:
        verbose_name = _("MPA")
        verbose_name_plural = _("MPAs")
        ordering = ("mpaname", "estyear")

    def __unicode__(self):
        return _("%s") % self.mpaname

    def __str__(self):
        return self.mpaname


class MPAInterviewYear(BaseModel):
    mpa = models.ForeignKey(MPA, on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(MAX_YEAR)]
    )

    class Meta:
        verbose_name = "MPA interview year"

    def __str__(self):
        return f"{self.mpa.name} {self.year}"


class MonitoringStaff(BaseModel):
    staffid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Settlement(BaseModel):
    TREATMENT_CHOICES = [(0, "Control"), (1, "Treatment")] + SKIP_CODES

    settlementid = models.IntegerField(primary_key=True)
    mpa = models.ForeignKey(MPA, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    treatment = models.PositiveSmallIntegerField(
        choices=TREATMENT_CHOICES, default=NODATA[0]
    )
    districtname = models.CharField(max_length=255)
    districtcode = models.BigIntegerField(blank=True, default=NODATA[0])
    marketname1 = models.CharField(max_length=255, default=str(NODATA[0]))
    marketname2 = models.CharField(max_length=255, default=str(NODATA[0]))
    zone = models.CharField(max_length=255, default=str(NODATA[0]))

    def __str__(self):
        return self.name


class LkpNoneToAllScale(BaseLookupModel):
    class Meta:
        ordering = ("code",)

    def __str__(self):
        return "{} [{}]".format(self.bahasaindonesia, self.english)
