from django.db import models


class Persons(models.Model):
    guid = models.CharField(primary_key=True, unique=True, editable=False, max_length=64)
    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=400)
    gender_female = models.IntegerField()
    snils_document = models.CharField(max_length=128)
    tab_number = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.full_name} ({self.tab_number})'

    class Meta:
        db_table = 'persons'
        managed = False
        ordering = ['full_name']


class Enterprises(models.Model):
    guid = models.CharField(primary_key=True, unique=True, max_length=64, db_column='guid')
    name = models.CharField(max_length=400, db_column='name')
    enterprise_code = models.IntegerField(db_column='enterprise_code')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'enterprises'
        managed = False
        ordering = ['enterprise_code']


    def get_list_shops(self):
        return Enterprises.objects.filter(enterprise_code__gte = 3, enterprise_code__lte = 999)



class persons_covid19(models.Model):
    uid = models.CharField(primary_key=True, unique=True, editable=False, max_length=64)
    enterprise_guid = models.ForeignKey(Enterprises, on_delete=models.CASCADE, db_column='enterprise_guid')
    person_guid = models.ForeignKey(Persons, on_delete=models.CASCADE, db_column='person_guid')
    dts = models.DateField(db_column='dts')
    vaccination_type = models.IntegerField()
    vaccination_declined = models.IntegerField()
    having_qr_code = models.IntegerField(db_column='having_qr_code')
    reply_code = models.IntegerField(db_column='reply_code')

    class Meta:
        db_table = 'persons_covid19'
        managed = False


class BusyKeys(models.Model):
    guid = models.CharField(primary_key=True, unique=True, max_length=64)
    short_name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=400)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = 'busy_keys'
        managed = False


class TimeSheetPlane(models.Model):
    p_uid = models.CharField(primary_key=True, unique=True, max_length=64, db_column='uid')
    enterprise_guid = models.ForeignKey(Enterprises, on_delete=models.CASCADE, db_column='enterprise_guid')
    person_guid = models.ForeignKey(Persons, on_delete=models.CASCADE, db_column='person_guid')
    dts = models.DateField()
    suspicious = models.IntegerField(db_column='suspicious')

    busy_key_guid = models.ForeignKey(BusyKeys, on_delete=models.CASCADE, db_column='busy_key_guid', verbose_name='Код')


    class Meta:
        db_table = 'shift_data_p'
        managed = False
        unique_together = (('p_uid', 'enterprise_guid', 'person_guid', 'dts'),)
        ordering = ['person_guid', 'dts']



class covid19_dtype(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    descr = models.CharField(max_length=512)

    class Meta:
        db_table = 'covid19_dtype'
        managed = False



class covid19_vtype(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    descr = models.CharField(max_length=512)

    class Meta:
        db_table = 'covid19_vtype'
        managed = False


class covid19_reply_codes(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    descr = models.CharField(max_length=128)

    class Meta:
        db_table = 'covid19_reply_codes'
        managed = False