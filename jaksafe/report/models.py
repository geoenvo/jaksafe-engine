from django.db import models
from django.db.models.fields import AutoField
from django.db.backends.mysql.creation import DatabaseCreation

# Create your models here.

class UnsignedAutoField(AutoField):
    def get_internal_type(self):
        return 'UnsignedAutoField'
        
DatabaseCreation.data_types['UnsignedAutoField'] = 'integer UNSIGNED AUTO_INCREMENT'

class AutoCalcDaily(models.Model):
    id = UnsignedAutoField(primary_key=True)
    id_event = models.PositiveIntegerField(null=True)
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    day = models.PositiveIntegerField(null=True)
    loss = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    
    class Meta:
        db_table = 'auto_calc_daily'
        
class AdHocCalc(models.Model):
    id = UnsignedAutoField(primary_key=True)
    id_event = models.PositiveIntegerField(null=True)
    id_user = models.IntegerField(null=True)
    id_user_group = models.IntegerField(null=True)
    t0 = models.DateTimeField()
    t1 = models.DateTimeField()
    damage = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    loss = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    
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
    id = UnsignedAutoField(primary_key=True)
    id_event = models.PositiveIntegerField(null=True)
    t0 = models.DateTimeField()
    t1 = models.DateTimeField()
    damage = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    loss = models.DecimalField(max_digits=17, decimal_places=2, null=True)
    
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
    damage = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    loss = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=17, decimal_places=2, default=0.00)

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
    id = UnsignedAutoField(primary_key=True)
    unit = models.CharField(max_length=255)
    village = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    rt = models.CharField(max_length=255, null=True)
    rw = models.CharField(max_length=255, null=True)
    depth = models.PositiveIntegerField()
    report_time = models.DateTimeField()
    request_time = models.DateTimeField()
    
    class Meta:
        db_table = 'fl_event'

class FloodEventRaw(models.Model):
    id = UnsignedAutoField(primary_key=True)
    unit = models.CharField(max_length=255)
    village = models.CharField(max_length=255, null=True)
    district = models.CharField(max_length=255, null=True)
    rt = models.CharField(max_length=255, null=True)
    rw = models.CharField(max_length=255, null=True)
    depth = models.PositiveIntegerField()
    report_time = models.DateTimeField()
    request_time = models.DateTimeField()
    
    class Meta:
        db_table = 'fl_event_raw'
