# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    id_admin = models.AutoField(db_column='Id_admin', primary_key=True)  # Field name made lowercase.
    name_admin = models.CharField(db_column='Name_admin', max_length=50)  # Field name made lowercase.
    family_name = models.CharField(db_column='Family_name', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=50)  # Field name made lowercase.
    password_admin = models.CharField(db_column='Password_admin', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'
    def __str__(self):
        return f"{self.family_name}"

class Client(models.Model):
    id_client = models.AutoField(db_column='Id_client', primary_key=True)  # Field name made lowercase.
    name_client = models.CharField(max_length=50)
    email_client = models.CharField(db_column='Email_client', unique=True, max_length=50)  # Field name made lowercase.
    n_tel = models.CharField(db_column='N_tel', max_length=50)  # Field name made lowercase.
    

    class Meta:
        managed = False
        db_table = 'client'
    def __str__(self):
        return f"{self.email_client}"

class Creneau(models.Model):
    id_creneau = models.AutoField(db_column='Id_creneau', primary_key=True)  # Field name made lowercase.
    date_a = models.DateField(db_column='Date_a')  # Field name made lowercase.
    heure_a = models.TimeField(db_column='Heure_a')  # Field name made lowercase.
    taken = models.IntegerField(blank=True, null=True)
    type_team = models.ForeignKey('Team', models.DO_NOTHING, db_column='Type_team')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'creneau'
    def __str__(self):
        return f"{self.date_a}"

class Employee(models.Model):
    email_emp = models.CharField(db_column='Email_emp', primary_key=True, max_length=50)  # Field name made lowercase.
    name_emp = models.CharField(db_column='Name_emp', max_length=50)  # Field name made lowercase.
    password_emp = models.CharField(db_column='Password_emp', max_length=50)  # Field name made lowercase.
    num_tel = models.CharField(db_column='Num_tel', max_length=50)  # Field name made lowercase.
    type_team = models.ForeignKey('Team', models.DO_NOTHING, db_column='Type_team')  # Field name made lowercase.
    id_admin = models.ForeignKey(Admin, models.DO_NOTHING, db_column='Id_admin')  # Field name made lowercase.
    photo=models.ImageField(upload_to='employees/',blank=True)
    class Meta:
        managed = False
        db_table = 'employee'
    def __str__(self):
        return f"{self.email_emp}"

class Events(models.Model):
    id_event = models.AutoField(db_column='Id_event', primary_key=True)  # Field name made lowercase.
    name_event = models.CharField(db_column='Name_event', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_event = models.DateField(db_column='Date_event')  # Field name made lowercase.
    heure_event = models.TimeField(db_column='Heure_event')  # Field name made lowercase.
    id_creneau = models.ForeignKey(Creneau, models.DO_NOTHING, db_column='Id_creneau')  # Field name made lowercase.
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='Id_client')  # Field name made lowercase.
    type_team = models.ForeignKey('Team', models.DO_NOTHING, db_column='Type_team')  # Field name made lowercase.
    finished=models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'events'
    def __str__(self):
        return f"{self.name_event}"

class Team(models.Model):
    type_team = models.CharField(db_column='Type_team', primary_key=True, max_length=50)  # Field name made lowercase.
    nbr_employee = models.IntegerField(db_column='Nbr_employee', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'team'
    def __str__(self):
        return f"{self.type_team}"
