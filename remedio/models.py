# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Dis(models.Model):
    disid = models.IntegerField(primary_key=True)
    disease = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dis'


class Relate(models.Model):
    id = models.IntegerField(primary_key=True)
    disid = models.ForeignKey(Dis, models.DO_NOTHING, db_column='disid', blank=True, null=True)
    symid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'relate'


class Symp(models.Model):
    symid = models.IntegerField(primary_key=True)
    symptom = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symp'


class Sympdis(models.Model):
    id = models.IntegerField(primary_key=True)
    medicine = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sympdis'

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING)
    sex = models.CharField(max_length=10,choices=[('male','Male'),('female','Female')])
    dob=models.DateField()
    def __str__(self):
        return self.user.username