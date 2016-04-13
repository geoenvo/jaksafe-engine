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

class AutoResultJSON(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    kelurahan_id = models.CharField(max_length=200)
    kota = models.CharField(max_length=200)
    kecamatan = models.CharField(max_length=200)
    kelurahan = models.CharField(max_length=200)
    rw = models.CharField(max_length=200)
    tanggal = models.DateTimeField()
    damage_infrastuktur = models.DecimalField(max_digits=17, decimal_places=2)
    loss_infrastruktur = models.DecimalField(max_digits=17, decimal_places=2)
    damage_lintas_sektor = models.DecimalField(max_digits=17, decimal_places=2)
    loss_lintas_sektor = models.DecimalField(max_digits=17, decimal_places=2)
    damage_produktif = models.DecimalField(max_digits=17, decimal_places=2)
    loss_produktif = models.DecimalField(max_digits=17, decimal_places=2)
    damage_sosial_perumahan = models.DecimalField(max_digits=17, decimal_places=2)
    loss_sosial_perumahan = models.DecimalField(max_digits=17, decimal_places=2)
    damage_total = models.DecimalField(max_digits=17, decimal_places=2)
    loss_total = models.DecimalField(max_digits=17, decimal_places=2)
    sumber = models.CharField(max_length=200)
    
class FloodEvent(models.Model):
    id = models.IntegerField(primary_key=True)
    unit = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    rt = models.CharField(max_length=255)
    rw = models.CharField(max_length=255)
    depth = models.IntegerField()
    report_time = models.DateTimeField()
    request_time = models.DateTimeField()
    
    class Meta:
        db_table = 'fl_event'

class FloodEventRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    unit = models.CharField(max_length=255)
    village = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    rt = models.CharField(max_length=255)
    rw = models.CharField(max_length=255)
    depth = models.IntegerField()
    report_time = models.DateTimeField()
    request_time = models.DateTimeField()
    
    class Meta:
        db_table = 'fl_event_raw'
