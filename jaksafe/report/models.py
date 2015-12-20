from django.db import models

# Create your models here.
	
class AdHocCalc(models.Model):
    id = models.IntegerField(primary_key=True)
    t0 = models.DateTimeField()
    t1 = models.DateTimeField()
    damage = models.DecimalField(max_digits=17, decimal_places=2)
    loss = models.DecimalField(max_digits=17, decimal_places=2)
    id_event = models.IntegerField()
    id_user = models.IntegerField()
    id_user_group = models.IntegerField()
	
    class Meta:
        db_table = 'adhoc_calc' 
		
class AdhocResult(models.Model):
    id_event = models.IntegerField()
    sector = models.CharField(max_length=200)
    subsector = models.CharField(max_length=200)
    asset = models.CharField(max_length=200)
    rw = models.CharField(max_length=3)
    kelurahan = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kota = models.CharField(max_length=50)
    kelas = models.CharField(max_length=50)
    damage = models.DecimalField(max_digits=17, decimal_places=2)
    loss = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        db_table = 'adhoc_dala_result'

class AutoCalc(models.Model):
    id = models.IntegerField(primary_key=True)
    id_event = models.IntegerField()
    t0 = models.DateTimeField()
    t1 = models.DateTimeField()
    damage = models.DecimalField(max_digits=17, decimal_places=2)
    loss = models.DecimalField(max_digits=17, decimal_places=2)
	
    class Meta:
        db_table = 'auto_calc' 
		
class AutoResult(models.Model):
    id_event = models.IntegerField()
    sector = models.CharField(max_length=200)
    subsector = models.CharField(max_length=200)
    asset = models.CharField(max_length=200)
    rw = models.CharField(max_length=3)
    kelurahan = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kota = models.CharField(max_length=50)
    kelas = models.CharField(max_length=50)
    damage = models.DecimalField(max_digits=17, decimal_places=2)
    loss = models.DecimalField(max_digits=17, decimal_places=2)

    class Meta:
        db_table = 'auto_dala_result'