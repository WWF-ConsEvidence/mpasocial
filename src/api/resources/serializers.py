from rest_framework import serializers
from ..models import *
from ..reports.report_serializer import ReportSerializer
from ..reports.fields import ReportField


class BaseFGDJSONSerializer(serializers.ModelSerializer):
    mpa = serializers.ReadOnlyField()


class BaseHouseholdJSONSerializer(serializers.ModelSerializer):
    mpa = serializers.ReadOnlyField()


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = []


class CountrySerializerCSV(ReportSerializer):
    class Meta:
        model = Country


class MPASerializer(serializers.ModelSerializer):
    class Meta:
        model = MPA
        exclude = []


class MPASerializerCSV(ReportSerializer):
    class Meta:
        model = MPA


class FGDSerializer(BaseFGDJSONSerializer):
    class Meta:
        model = FGD
        exclude = []


class FGDSerializerCSV(ReportSerializer):
    fields = [
        ReportField("fgdid", "fgdid"),
        ReportField("settlement__mpa", "mpa"),
        ReportField("settlement", "settlement"),
        ReportField("fgdcode", "fgdcode"),
        ReportField("facilitator", "facilitator"),
        ReportField("notetaker", "notetaker"),
        ReportField("fgdate", "fgdate"),
        ReportField("yearmonitoring", "yearmonitoring"),
        ReportField("starttime", "starttime"),
        ReportField("endtime", "endtime"),
        ReportField("maleparticipants", "maleparticipants"),
        ReportField("femaleparticipants", "femaleparticipants"),
        ReportField("fgdversion", "fgdversion"),
        ReportField("fgroundname", "fgroundname"),
        ReportField("fgroundboat", "fgroundboat"),
        ReportField("fgroundtime", "fgroundtime"),
        ReportField("fgrounddist", "fgrounddist"),
        ReportField("fgroundsize", "fgroundsize"),
        ReportField("mpaname", "mpaname"),
        ReportField("mpaboat", "mpaboat"),
        ReportField("mpatime", "mpatime"),
        ReportField("mpadist", "mpadist"),
        ReportField("mpasize", "mpasize"),
        ReportField("ntname", "ntname"),
        ReportField("ntboat", "ntboat"),
        ReportField("nttime", "nttime"),
        ReportField("ntdist", "ntdist"),
        ReportField("ntsize", "ntsize"),
        ReportField("mpahistl", "mpahistl"),
        ReportField("mpahist", "mpahist"),
        ReportField("extbnd", "extbnd"),
        ReportField("intbnd", "intbnd"),
        ReportField("bndlandmarks", "bndlandmarks"),
        ReportField("bndmarkers", "bndmarkers"),
        ReportField("bndsigns", "bndsigns"),
        ReportField("bndgovnotice", "bndgovnotice"),
        ReportField("bndwoutreach", "bndwoutreach"),
        ReportField("bndaoutreach", "bndaoutreach"),
        ReportField("bndvoutreach", "bndvoutreach"),
        ReportField("bndword", "bndword"),
        ReportField("bndotheroutreach", "bndotheroutreach"),
        ReportField("bndother", "bndother"),
        ReportField("bndotherspecifyl", "bndotherspecifyl"),
        ReportField("bndotherspecify", "bndotherspecify"),
        ReportField("penaltyverbal", "penaltyverbal"),
        ReportField("penaltywritten", "penaltywritten"),
        ReportField("penaltyaccess", "penaltyaccess"),
        ReportField("penaltyequipment", "penaltyequipment"),
        ReportField("penaltyfines", "penaltyfines"),
        ReportField("penaltyprison", "penaltyprison"),
        ReportField("penaltyother", "penaltyother"),
        ReportField("penaltyotherspecifyl", "penaltyotherspecifyl"),
        ReportField("penaltyotherspecify", "penaltyotherspecify"),
        ReportField("npenalty", "npenalty"),
        ReportField("verbalsanction", "verbalsanction"),
        ReportField("physicalsanction", "physicalsanction"),
        ReportField("monetarysanction", "monetarysanction"),
        ReportField("conflictl", "conflictl"),
        ReportField("conflict", "conflict"),
        ReportField("conflictusertime", "conflictusertime"),
        ReportField("conflictofficialtime", "conflictofficialtime"),
        ReportField("conflictusercost", "conflictusercost"),
        ReportField("conflictofficialcost", "conflictofficialcost"),
        ReportField("conflictuserdist", "conflictuserdist"),
        ReportField("conflictofficialdist", "conflictofficialdist"),
        ReportField("otherinfol", "otherinfol"),
        ReportField("otherinfo", "otherinfo"),
        ReportField("otherpeoplel", "otherpeoplel"),
        ReportField("otherpeople", "otherpeople"),
        ReportField("othersourcesl", "othersourcesl"),
        ReportField("othersources", "othersources"),
        ReportField("traditionalgovernancel", "traditionalgovernancel"),
        ReportField("traditionalgovernance", "traditionalgovernance"),
        ReportField("conflictn", "conflictn"),
        ReportField("congroup", "congroup"),
        ReportField("conbtwgroups", "conbtwgroups"),
        ReportField("conbtwgroupngov", "conbtwgroupngov"),
        ReportField("congov", "congov"),
        ReportField("contypemarine", "contypemarine"),
        ReportField("contypegov", "contypegov"),
        ReportField("contypeusers", "contypeusers"),
        ReportField("contyperec", "contyperec"),
        ReportField("contypeother", "contypeother"),
        ReportField("contypeotherspecifyl", "contypeotherspecifyl"),
        ReportField("contypeotherspecify", "contypeotherspecify"),
        ReportField("dataentryid", "dataentryid"),
        ReportField("datacheckid", "datacheckid"),
        ReportField("notesl", "notesl"),
        ReportField("notes", "notes"),
        ReportField("qaqcnotes", "qaqcnotes"),
        ReportField("fgdid", "fgdid"),
        ReportField("settlement", "settlement"),
        ReportField("fgdcode", "fgdcode"),
        ReportField("facilitator", "facilitator"),
        ReportField("notetaker", "notetaker"),
        ReportField("fgdate", "fgdate"),
        ReportField("yearmonitoring", "yearmonitoring"),
        ReportField("starttime", "starttime"),
        ReportField("endtime", "endtime"),
        ReportField("maleparticipants", "maleparticipants"),
        ReportField("femaleparticipants", "femaleparticipants"),
        ReportField("fgdversion", "fgdversion"),
        ReportField("fgroundname", "fgroundname"),
        ReportField("fgroundboat", "fgroundboat"),
        ReportField("fgroundtime", "fgroundtime"),
        ReportField("fgrounddist", "fgrounddist"),
        ReportField("fgroundsize", "fgroundsize"),
        ReportField("mpaname", "mpaname"),
        ReportField("mpaboat", "mpaboat"),
        ReportField("mpatime", "mpatime"),
        ReportField("mpadist", "mpadist"),
        ReportField("mpasize", "mpasize"),
        ReportField("ntname", "ntname"),
        ReportField("ntboat", "ntboat"),
        ReportField("nttime", "nttime"),
        ReportField("ntdist", "ntdist"),
        ReportField("ntsize", "ntsize"),
        ReportField("mpahistl", "mpahistl"),
        ReportField("mpahist", "mpahist"),
        ReportField("extbnd", "extbnd"),
        ReportField("intbnd", "intbnd"),
        ReportField("bndlandmarks", "bndlandmarks"),
        ReportField("bndmarkers", "bndmarkers"),
        ReportField("bndsigns", "bndsigns"),
        ReportField("bndgovnotice", "bndgovnotice"),
        ReportField("bndwoutreach", "bndwoutreach"),
        ReportField("bndaoutreach", "bndaoutreach"),
        ReportField("bndvoutreach", "bndvoutreach"),
        ReportField("bndword", "bndword"),
        ReportField("bndotheroutreach", "bndotheroutreach"),
        ReportField("bndother", "bndother"),
        ReportField("bndotherspecifyl", "bndotherspecifyl"),
        ReportField("bndotherspecify", "bndotherspecify"),
        ReportField("penaltyverbal", "penaltyverbal"),
        ReportField("penaltywritten", "penaltywritten"),
        ReportField("penaltyaccess", "penaltyaccess"),
        ReportField("penaltyequipment", "penaltyequipment"),
        ReportField("penaltyfines", "penaltyfines"),
        ReportField("penaltyprison", "penaltyprison"),
        ReportField("penaltyother", "penaltyother"),
        ReportField("penaltyotherspecifyl", "penaltyotherspecifyl"),
        ReportField("penaltyotherspecify", "penaltyotherspecify"),
        ReportField("npenalty", "npenalty"),
        ReportField("verbalsanction", "verbalsanction"),
        ReportField("physicalsanction", "physicalsanction"),
        ReportField("monetarysanction", "monetarysanction"),
        ReportField("conflictl", "conflictl"),
        ReportField("conflict", "conflict"),
        ReportField("conflictusertime", "conflictusertime"),
        ReportField("conflictofficialtime", "conflictofficialtime"),
        ReportField("conflictusercost", "conflictusercost"),
        ReportField("conflictofficialcost", "conflictofficialcost"),
        ReportField("conflictuserdist", "conflictuserdist"),
        ReportField("conflictofficialdist", "conflictofficialdist"),
        ReportField("otherinfol", "otherinfol"),
        ReportField("otherinfo", "otherinfo"),
        ReportField("otherpeoplel", "otherpeoplel"),
        ReportField("otherpeople", "otherpeople"),
        ReportField("othersourcesl", "othersourcesl"),
        ReportField("othersources", "othersources"),
        ReportField("traditionalgovernancel", "traditionalgovernancel"),
        ReportField("traditionalgovernance", "traditionalgovernance"),
        ReportField("conflictn", "conflictn"),
        ReportField("congroup", "congroup"),
        ReportField("conbtwgroups", "conbtwgroups"),
        ReportField("conbtwgroupngov", "conbtwgroupngov"),
        ReportField("congov", "congov"),
        ReportField("contypemarine", "contypemarine"),
        ReportField("contypegov", "contypegov"),
        ReportField("contypeusers", "contypeusers"),
        ReportField("contyperec", "contyperec"),
        ReportField("contypeother", "contypeother"),
        ReportField("contypeotherspecifyl", "contypeotherspecifyl"),
        ReportField("contypeotherspecify", "contypeotherspecify"),
        ReportField("dataentryid", "dataentryid"),
        ReportField("datacheckid", "datacheckid"),
        ReportField("notesl", "notesl"),
        ReportField("notes", "notes"),
        ReportField("qaqcnotes", "qaqcnotes"),
    ]
    # additional_fields = [
    #     ReportField("settlement__mpa", "mpa"),
    # ]

    class Meta:
        model = FGD


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        exclude = []


class HabitatSerializerCSV(ReportSerializer):
    class Meta:
        model = Habitat


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        exclude = []


class RuleSerializerCSV(ReportSerializer):
    class Meta:
        model = Rule


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        exclude = []


class SpeciesSerializerCSV(ReportSerializer):
    class Meta:
        model = Species


class StakeholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        exclude = []


class StakeholderSerializerCSV(ReportSerializer):
    class Meta:
        model = Stakeholder


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        exclude = []


class SettlementSerializerCSV(ReportSerializer):
    class Meta:
        model = Settlement


class BirthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birth
        exclude = []


class BirthSerializerCSV(ReportSerializer):
    class Meta:
        model = Birth


class DeathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Death
        exclude = []


class DeathSerializerCSV(ReportSerializer):
    class Meta:
        model = Death


class DemographicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demographic
        exclude = []


class DemographicSerializerCSV(ReportSerializer):
    class Meta:
        model = Demographic


class GlobalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalStep
        exclude = []


class GlobalStepSerializerCSV(ReportSerializer):
    class Meta:
        model = GlobalStep


class GlobalThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalThreat
        exclude = []


class GlobalThreatSerializerCSV(ReportSerializer):
    class Meta:
        model = GlobalThreat


class LocalStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalStep
        exclude = []


class LocalStepSerializerCSV(ReportSerializer):
    class Meta:
        model = LocalStep


class LocalThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalThreat
        exclude = []


class LocalThreatSerializerCSV(ReportSerializer):
    class Meta:
        model = LocalThreat


class NonMarineOrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonMarineOrganizationMembership
        exclude = []


class NonMarineOrganizationMembershipSerializerCSV(ReportSerializer):
    class Meta:
        model = NonMarineOrganizationMembership


class MarineOrganizationMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarineOrganizationMembership
        exclude = []


class MarineOrganizationMembershipSerializerCSV(ReportSerializer):
    class Meta:
        model = MarineOrganizationMembership


class HouseholdSerializer(BaseHouseholdJSONSerializer):
    class Meta:
        model = Household
        exclude = []


class HouseholdSerializerCSV(ReportSerializer):
    fields = [
        ReportField("householdid", "householdid"),
        ReportField("settlement__mpa", "mpa"),
        ReportField("settlement", "settlement"),
        ReportField("kkcode", "kkcode"),
        ReportField("primaryinterviewer", "primaryinterviewer"),
        ReportField("secondaryinterviewer", "secondaryinterviewer"),
        ReportField("fieldcoordinator", "fieldcoordinator"),
        ReportField("yearmonitoring", "yearmonitoring"),
        ReportField("yearmonitoring", "yearmonitoring"),
        ReportField("interviewdate", "interviewdate"),
        ReportField("interviewstart", "interviewstart"),
        ReportField("interviewend", "interviewend"),
        ReportField("interviewlength", "interviewlength"),
        ReportField("surveyversionnumber", "surveyversionnumber"),
        ReportField("usualfish", "usualfish"),
        ReportField("householdsize", "householdsize"),
        ReportField("yearsresident", "yearsresident"),
        ReportField("timemarket", "timemarket"),
        ReportField("primarymarketname", "primarymarketname"),
        ReportField("secondarymarketname", "secondarymarketname"),
        ReportField("timesecondarymarket", "timesecondarymarket"),
        ReportField("paternalethnicity", "paternalethnicity"),
        ReportField("maternalethnicity", "maternalethnicity"),
        ReportField("religion", "religion"),
        ReportField("primarylivelihood", "primarylivelihood"),
        ReportField("primarylivelihoodyear", "primarylivelihoodyear"),
        ReportField("secondarylivelihood", "secondarylivelihood"),
        ReportField("secondarylivelihoodyear", "secondarylivelihoodyear"),
        ReportField("tertiarylivelihood", "tertiarylivelihood"),
        ReportField("tertiarylivelihoodyear", "tertiarylivelihoodyear"),
        ReportField("freqfishtime", "freqfishtime"),
        ReportField("freqsalefish", "freqsalefish"),
        ReportField("percentincomefish", "percentincomefish"),
        ReportField("freqeatfish", "freqeatfish"),
        ReportField("percentproteinfish", "percentproteinfish"),
        ReportField("majorfishtechnique", "majorfishtechnique"),
        ReportField("primaryfishtechnique", "primaryfishtechnique"),
        ReportField("secondaryfishtechnique", "secondaryfishtechnique"),
        ReportField("tertiaryfishtechnique", "tertiaryfishtechnique"),
        ReportField("lessproductivedaysfishing", "lessproductivedaysfishing"),
        ReportField("poorcatch", "poorcatch"),
        ReportField("poorcatchunits", "poorcatchunits"),
        ReportField("poorcatchunitscategory", "poorcatchunitscategory"),
        ReportField("poorfishincome", "poorfishincome"),
        ReportField("poorfishincomeunits", "poorfishincomeunits"),
        ReportField("moreproductivedaysfishing", "moreproductivedaysfishing"),
        ReportField("goodcatch", "goodcatch"),
        ReportField("goodcatchunits", "goodcatchunits"),
        ReportField("goodcatchunitscategory", "goodcatchunitscategory"),
        ReportField("goodfishincome", "goodfishincome"),
        ReportField("goodfishincomeunits", "goodfishincomeunits"),
        ReportField("economicstatustrend", "economicstatustrend"),
        ReportField("economicstatusreasonl", "economicstatusreasonl"),
        ReportField("economicstatusreason", "economicstatusreason"),
        ReportField("economicadjustreasonl", "economicadjustreasonl"),
        ReportField("economicadjustreason", "economicadjustreason"),
        ReportField("assetcar", "assetcar"),
        ReportField("assettruck", "assettruck"),
        ReportField("assetcartruck", "assetcartruck"),
        ReportField("assetbicycle", "assetbicycle"),
        ReportField("assetmotorcycle", "assetmotorcycle"),
        ReportField("assetboatnomotor", "assetboatnomotor"),
        ReportField("assetboatoutboard", "assetboatoutboard"),
        ReportField("assetboatinboard", "assetboatinboard"),
        ReportField("assetlandlinephone", "assetlandlinephone"),
        ReportField("assetcellphone", "assetcellphone"),
        ReportField("assetphonecombined", "assetphonecombined"),
        ReportField("assettv", "assettv"),
        ReportField("assetradio", "assetradio"),
        ReportField("assetstereo", "assetstereo"),
        ReportField("assetcd", "assetcd"),
        ReportField("assetdvd", "assetdvd"),
        ReportField("assetentertain", "assetentertain"),
        ReportField("assetsatellite", "assetsatellite"),
        ReportField("assetgenerator", "assetgenerator"),
        ReportField("cookingfuel", "cookingfuel"),
        ReportField("householddeath", "householddeath"),
        ReportField("householdbirth", "householdbirth"),
        ReportField("fsnotenough", "fsnotenough"),
        ReportField("fsdidnotlast", "fsdidnotlast"),
        ReportField("fsbalanceddiet", "fsbalanceddiet"),
        ReportField("fsadultskip", "fsadultskip"),
        ReportField("fsfreqadultskip", "fsfreqadultskip"),
        ReportField("fseatless", "fseatless"),
        ReportField("fshungry", "fshungry"),
        ReportField("fschildportion", "fschildportion"),
        ReportField("fslowcostfood", "fslowcostfood"),
        ReportField("fschildskip", "fschildskip"),
        ReportField("fsfreqchildskip", "fsfreqchildskip"),
        ReportField("fsnomealchild", "fsnomealchild"),
        ReportField("rightsaccess", "rightsaccess"),
        ReportField("rightsharvest", "rightsharvest"),
        ReportField("rightsmanage", "rightsmanage"),
        ReportField("rightsexclude", "rightsexclude"),
        ReportField("rightstransfer", "rightstransfer"),
        ReportField("socialconflict", "socialconflict"),
        ReportField("marinegroup", "marinegroup"),
        ReportField("numbermarinegroup", "numbermarinegroup"),
        ReportField("othergroup", "othergroup"),
        ReportField("numberothergroup", "numberothergroup"),
        ReportField("votedistrict", "votedistrict"),
        ReportField("votenational", "votenational"),
        ReportField("numlocalthreat", "numlocalthreat"),
        ReportField("numglobalthreat", "numglobalthreat"),
        ReportField("numlocalaction", "numlocalaction"),
        ReportField("numglobalaction", "numglobalaction"),
        ReportField("placehappy", "placehappy"),
        ReportField("placefavourite", "placefavourite"),
        ReportField("placemiss", "placemiss"),
        ReportField("placebest", "placebest"),
        ReportField("placefishhere", "placefishhere"),
        ReportField("placebemyself", "placebemyself"),
        ReportField("anyotherinfo", "anyotherinfo"),
        ReportField("willingparticipant", "willingparticipant"),
        ReportField("notes", "notes"),
        ReportField("dataentrycomplete", "dataentrycomplete"),
        ReportField("datacheckcomplete", "datacheckcomplete"),
        ReportField("dataentryid", "dataentryid"),
        ReportField("datacheckid", "datacheckid"),
        ReportField("worstdaycatch", "worstdaycatch"),
        ReportField("worstdaycatchunits", "worstdaycatchunits"),
        ReportField("bestdaycatch", "bestdaycatch"),
        ReportField("bestdaycatchunits", "bestdaycatchunits"),
        ReportField("averageincome", "averageincome"),
        ReportField("averageincomeunits", "averageincomeunits"),
        ReportField("worstincome", "worstincome"),
        ReportField("worstincomeunits", "worstincomeunits"),
        ReportField("bestincome", "bestincome"),
        ReportField("bestincomeunits", "bestincomeunits"),
        ReportField("entrycomputeridentifier", "entrycomputeridentifier"),
        ReportField("entryhouseholdid", "entryhouseholdid"),
        ReportField("pilotreferencecode", "pilotreferencecode"),
        ReportField("baseline_t2_pairs", "baseline_t2_pairs"),
    ]
    # additional_fields = [
    #     ReportField("settlement__mpa", "mpa"),
    # ]

    class Meta:
        model = Household


class KIISerializer(serializers.ModelSerializer):
    class Meta:
        model = KII
        exclude = []


class KIISerializerCSV(ReportSerializer):
    fields = [
        ReportField("kiiid", "kiiid"),
        ReportField("settlement__mpa", "mpa"),
        ReportField("settlement", "settlement"),
        ReportField("kiicode", "kiicode"),
        ReportField("fgd", "fgd"),
        ReportField("keyinformantrole", "keyinformantrole"),
        ReportField("primaryinterviewer", "primaryinterviewer"),
        ReportField("secondaryinterviewer", "secondaryinterviewer"),
        ReportField("kiidate", "kiidate"),
        ReportField("yearmonitoring", "yearmonitoring"),
        ReportField("starttime", "starttime"),
        ReportField("endtime", "endtime"),
        ReportField("kiiversion", "kiiversion"),
        ReportField("mpahistoryl", "mpahistoryl"),
        ReportField("mpahistory", "mpahistory"),
        ReportField("pilotnzones", "pilotnzones"),
        ReportField("ecozone", "ecozone"),
        ReportField("soczone", "soczone"),
        ReportField("druleeco", "druleeco"),
        ReportField("drulesoc", "drulesoc"),
        ReportField("pilotnestedness", "pilotnestedness"),
        ReportField("rulecomml", "rulecomml"),
        ReportField("rulecomm", "rulecomm"),
        ReportField("ruleawarel", "ruleawarel"),
        ReportField("ruleaware", "ruleaware"),
        ReportField("rulepracticel", "rulepracticel"),
        ReportField("rulepractice", "rulepractice"),
        ReportField("informalrulel", "informalrulel"),
        ReportField("informalrule", "informalrule"),
        ReportField("ruleparticipationl", "ruleparticipationl"),
        ReportField("ruleparticipation", "ruleparticipation"),
        ReportField("monitorl", "monitorl"),
        ReportField("monitor", "monitor"),
        ReportField("penverbal", "penverbal"),
        ReportField("penwritten", "penwritten"),
        ReportField("penaccess", "penaccess"),
        ReportField("penequipment", "penequipment"),
        ReportField("penfines", "penfines"),
        ReportField("penincarceraton", "penincarceraton"),
        ReportField("penother", "penother"),
        ReportField("penotherspecifyl", "penotherspecifyl"),
        ReportField("penotherspecify", "penotherspecify"),
        ReportField("penfreq", "penfreq"),
        ReportField("penprevious", "penprevious"),
        ReportField("peneco", "peneco"),
        ReportField("penecon", "penecon"),
        ReportField("pensoc", "pensoc"),
        ReportField("penwealth", "penwealth"),
        ReportField("penpower", "penpower"),
        ReportField("penstatus", "penstatus"),
        ReportField("penfactorother", "penfactorother"),
        ReportField("penfactorotherspecifyl", "penfactorotherspecifyl"),
        ReportField("penfactorotherspecify", "penfactorotherspecify"),
        ReportField("incened", "incened"),
        ReportField("incenskills", "incenskills"),
        ReportField("incenequipment", "incenequipment"),
        ReportField("incenpurchase", "incenpurchase"),
        ReportField("incenloan", "incenloan"),
        ReportField("incenpayment", "incenpayment"),
        ReportField("incenemploy", "incenemploy"),
        ReportField("incenother", "incenother"),
        ReportField("incenotherspecifyl", "incenotherspecifyl"),
        ReportField("incenotherspecify", "incenotherspecify"),
        ReportField("ecomonverbal", "ecomonverbal"),
        ReportField("ecomonwritten", "ecomonwritten"),
        ReportField("ecomonaccess", "ecomonaccess"),
        ReportField("ecomonposition", "ecomonposition"),
        ReportField("ecomonequipment", "ecomonequipment"),
        ReportField("ecomonfine", "ecomonfine"),
        ReportField("ecomonincarceration", "ecomonincarceration"),
        ReportField("ecomonother", "ecomonother"),
        ReportField("ecomonotherspecifyl", "ecomonotherspecifyl"),
        ReportField("ecomonotherspecify", "ecomonotherspecify"),
        ReportField("socmonverbal", "socmonverbal"),
        ReportField("socmonwritten", "socmonwritten"),
        ReportField("socmonaccess", "socmonaccess"),
        ReportField("socmonposition", "socmonposition"),
        ReportField("socmonequipment", "socmonequipment"),
        ReportField("socmonfine", "socmonfine"),
        ReportField("socmonincarceration", "socmonincarceration"),
        ReportField("socmonother", "socmonother"),
        ReportField("socmonotherspecifyl", "socmonotherspecifyl"),
        ReportField("socmonotherspecify", "socmonotherspecify"),
        ReportField("compmonverbal", "compmonverbal"),
        ReportField("compmonwritten", "compmonwritten"),
        ReportField("compmonaccess", "compmonaccess"),
        ReportField("compmonposition", "compmonposition"),
        ReportField("compmonequipment", "compmonequipment"),
        ReportField("compmonfine", "compmonfine"),
        ReportField("compmonincarceration", "compmonincarceration"),
        ReportField("compmonother", "compmonother"),
        ReportField("compmonotherspecifyl", "compmonotherspecifyl"),
        ReportField("compmonotherspecify", "compmonotherspecify"),
        ReportField("penmonverbal", "penmonverbal"),
        ReportField("penmonwritten", "penmonwritten"),
        ReportField("penmonaccess", "penmonaccess"),
        ReportField("penmonposition", "penmonposition"),
        ReportField("penmonequipment", "penmonequipment"),
        ReportField("penmonfine", "penmonfine"),
        ReportField("penmonincarceration", "penmonincarceration"),
        ReportField("penmonother", "penmonother"),
        ReportField("penmonotherspecifyl", "penmonotherspecifyl"),
        ReportField("penmonotherspecify", "penmonotherspecify"),
        ReportField("conflictresl", "conflictresl"),
        ReportField("conflictres", "conflictres"),
        ReportField("ecoimpactl", "ecoimpactl"),
        ReportField("ecoimpact", "ecoimpact"),
        ReportField("socimpactl", "socimpactl"),
        ReportField("socimpact", "socimpact"),
        ReportField("contributionl", "contributionl"),
        ReportField("contribution", "contribution"),
        ReportField("benefitl", "benefitl"),
        ReportField("benefit", "benefit"),
        ReportField("ecoimpactcovidl", "ecoimpactcovidl"),
        ReportField("ecoimpactcovid", "ecoimpactcovid"),
        ReportField("socimpactcovidl", "socimpactcovidl"),
        ReportField("socimpactcovid", "socimpactcovid"),
        ReportField("mpaimpactcovidl", "mpaimpactcovidl"),
        ReportField("mpaimpactcovid", "mpaimpactcovid"),
        ReportField("anyotherinfol", "anyotherinfol"),
        ReportField("anyotherinfo", "anyotherinfo"),
        ReportField("anyotherkil", "anyotherkil"),
        ReportField("anyotherki", "anyotherki"),
        ReportField("anyotherdocsl", "anyotherdocsl"),
        ReportField("anyotherdocs", "anyotherdocs"),
        ReportField("notesl", "notesl"),
        ReportField("notes", "notes"),
        ReportField("dataentryid", "dataentryid"),
        ReportField("datacheckid", "datacheckid"),
        ReportField("violationfreq", "violationfreq"),
    ]
    # additional_fields = [
    #     ReportField("settlement__mpa", "mpa"),
    # ]

    class Meta:
        model = KII


class HabitatRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitatRule
        exclude = []


class HabitatRuleSerializerCSV(ReportSerializer):
    class Meta:
        model = HabitatRule


class RightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Right
        exclude = []


class RightSerializerCSV(ReportSerializer):
    class Meta:
        model = Right


class SpeciesRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesRule
        exclude = []


class SpeciesRuleSerializerCSV(ReportSerializer):
    class Meta:
        model = SpeciesRule


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        exclude = []


class ZoneSerializerCSV(ReportSerializer):
    class Meta:
        model = Zone


class LookupSerializerMixin(object):
    class Meta:
        exclude = ["created_on", "updated_on", "updated_by"]


class MonitoringStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringStaff
        exclude = []


class MonitoringStaffSerializerCSV(ReportSerializer):
    class Meta:
        model = MonitoringStaff


class LkpAssetAssistanceSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpAssetAssistance


class LkpAssetObtainSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpAssetObtain


class LkpFreqFishTimeSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpFreqFishTime


class LkpFishTechCategorySerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpFishTechCategory


class LkpFishTechniqueSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpFishTechnique


class LkpLivelihoodSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpLivelihood


class LkpNoneToAllScaleSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = LkpNoneToAllScale


class LkpMPANetworkSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = MPANetwork


class LkpSeascapeSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = Seascape


class HouseholdSurveyVersionSerializer(
    LookupSerializerMixin, serializers.ModelSerializer
):
    class Meta(LookupSerializerMixin.Meta):
        model = HouseholdSurveyVersion


class FGDSurveyVersionSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = FGDSurveyVersion


class KIISurveyVersionSerializer(LookupSerializerMixin, serializers.ModelSerializer):
    class Meta(LookupSerializerMixin.Meta):
        model = KIISurveyVersion
