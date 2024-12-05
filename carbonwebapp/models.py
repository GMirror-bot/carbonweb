from django.db import models

class UserInfo(models.Model):
    UID = models.AutoField(primary_key=True)
    User = models.CharField(max_length=64, null=True, blank=True)
    Pass = models.CharField(max_length=64, null=True, blank=True)
    Mail = models.CharField(max_length=64, null=True, blank=True)
    authority = models.CharField(max_length=64, null=True, blank=True)

class FactorCalssInfo(models.Model):
    FactorCalssID = models.AutoField(primary_key=True)
    FactorCalssName = models.CharField(max_length=64, null=True, blank=True)


class FactorInfo(models.Model):
    FactorID = models.AutoField(primary_key=True)
    FactorName = models.CharField(max_length=64, null=True, blank=True)
    FactorCalssID = models.IntegerField(null=True, blank=True)
    FactorNum = models.FloatField(null=True, blank=True)
    FactorUnit = models.CharField(max_length=64, null=True, blank=True)
    FactorSource = models.CharField(max_length=64, null=True, blank=True)

class FormulaInfo(models.Model):
    FormulaID = models.AutoField(primary_key=True)
    cement = models.FloatField(null=True, blank=True)
    GBFS = models.FloatField(null=True, blank=True)
    FA = models.FloatField(null=True, blank=True)
    water = models.FloatField(null=True, blank=True)
    FAggregate = models.FloatField(null=True, blank=True)
    CAggregate = models.FloatField(null=True, blank=True)
    Superplasticizer = models.FloatField(null=True, blank=True)

class StrengthInfo(models.Model):
    StrengID = models.AutoField(primary_key=True)
    FormulaID = models.IntegerField(null=True, blank=True)
    age = models.FloatField(null=True, blank=True)
    Strength = models.FloatField(null=True, blank=True)

class ModelsInfo(models.Model):
    ModelID = models.AutoField(primary_key=True)
    ModelName = models.CharField(max_length=64, null=True, blank=True)
    Modelpath = models.CharField(max_length=128, null=True, blank=True)

class OptimizeInfo(models.Model):
    OptimizeID = models.AutoField(primary_key=True)
    TargetDay= models.FloatField(null=True, blank=True)
    TargetStrength= models.FloatField(null=True, blank=True)
    TargetSlump= models.FloatField(null=True, blank=True)
    bestCost= models.FloatField(null=True, blank=True)
    bestCarbon= models.FloatField(null=True, blank=True)
    bestCostFormulaID= models.IntegerField(null=True, blank=True)
    bestCarbonFormulaID= models.IntegerField(null=True, blank=True)

class FormulaCompareInfo(models.Model):
    CompareID = models.AutoField(primary_key=True)
    OptimizeID= models.IntegerField(null=True, blank=True)
    FormulaID = models.IntegerField(null=True, blank=True)
    FormulaPrice= models.FloatField(null=True, blank=True)
    carbonFormula= models.FloatField(null=True, blank=True)

class PriceInfo(models.Model):
    OptimizeID = models.IntegerField(primary_key=True)
    time =  models.CharField(max_length=128, null=True, blank=True)
    cement= models.FloatField(null=True, blank=True)
    GBFS= models.FloatField(null=True, blank=True)
    FA= models.FloatField(null=True, blank=True)
    water= models.FloatField(null=True, blank=True)
    FAggregate= models.FloatField(null=True, blank=True)
    CAggregate= models.FloatField(null=True, blank=True)
    Superplasticizer= models.FloatField(null=True, blank=True)

class carbonInfo(models.Model):
    OptimizeID = models.IntegerField(primary_key=True)
    time =  models.CharField(max_length=128, null=True, blank=True)
    cement= models.FloatField(null=True, blank=True)
    GBFS= models.FloatField(null=True, blank=True)
    FA= models.FloatField(null=True, blank=True)
    water= models.FloatField(null=True, blank=True)
    FAggregate= models.FloatField(null=True, blank=True)
    CAggregate= models.FloatField(null=True, blank=True)
    Superplasticizer= models.FloatField(null=True, blank=True)
# Create your models here.
