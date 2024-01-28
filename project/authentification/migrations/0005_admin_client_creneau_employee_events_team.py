# Generated by Django 2.2.28 on 2023-12-31 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentification', '0004_auto_20231227_0034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id_admin', models.AutoField(db_column='Id_admin', primary_key=True, serialize=False)),
                ('name_admin', models.CharField(db_column='Name_admin', max_length=50)),
                ('family_name', models.CharField(db_column='Family_name', max_length=50)),
                ('email', models.CharField(db_column='Email', max_length=50, unique=True)),
                ('password_admin', models.CharField(db_column='Password_admin', max_length=50)),
            ],
            options={
                'db_table': 'admin',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id_client', models.AutoField(db_column='Id_client', primary_key=True, serialize=False)),
                ('fname_client', models.CharField(max_length=50)),
                ('email_client', models.CharField(db_column='Email_client', max_length=50, unique=True)),
                ('lname_client', models.CharField(max_length=50)),
                ('n_tel', models.CharField(db_column='N_tel', max_length=50)),
                ('password_client', models.CharField(db_column='Password_client', max_length=50)),
            ],
            options={
                'db_table': 'client',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Creneau',
            fields=[
                ('id_creneau', models.AutoField(db_column='Id_creneau', primary_key=True, serialize=False)),
                ('date_a', models.DateField(db_column='Date_a')),
                ('heure_a', models.TimeField(db_column='Heure_a')),
                ('taken', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'creneau',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('email_emp', models.CharField(db_column='Email_emp', max_length=50, primary_key=True, serialize=False)),
                ('name_emp', models.CharField(db_column='Name_emp', max_length=50)),
                ('password_emp', models.CharField(db_column='Password_emp', max_length=50)),
                ('num_tel', models.CharField(db_column='Num_tel', max_length=50)),
            ],
            options={
                'db_table': 'employee',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id_event', models.AutoField(db_column='Id_event', primary_key=True, serialize=False)),
                ('name_event', models.CharField(db_column='Name_event', max_length=50)),
                ('description', models.CharField(blank=True, db_column='Description', max_length=50, null=True)),
                ('date_event', models.DateField(db_column='Date_event')),
                ('heure_event', models.TimeField(db_column='Heure_event')),
            ],
            options={
                'db_table': 'events',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('type_team', models.CharField(db_column='Type_team', max_length=50, primary_key=True, serialize=False)),
                ('nbr_employee', models.IntegerField(blank=True, db_column='Nbr_employee', null=True)),
            ],
            options={
                'db_table': 'team',
                'managed': False,
            },
        ),
    ]