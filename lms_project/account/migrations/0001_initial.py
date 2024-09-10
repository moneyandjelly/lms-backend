# Generated by Django 5.0.7 on 2024-09-02 07:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAttendanceCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Attendance_cherry', models.IntegerField(default=0)),
                ('Attendance_date1', models.IntegerField(default=0)),
                ('Attendance_date2', models.IntegerField(default=0)),
                ('Attendance_date3', models.IntegerField(default=0)),
                ('Attendance_date4', models.IntegerField(default=0)),
                ('Attendance_date5', models.IntegerField(default=0)),
                ('Attendance_date6', models.IntegerField(default=0)),
                ('Attendance_date7', models.IntegerField(default=0)),
                ('Attendance_date8', models.IntegerField(default=0)),
                ('Attendance_date9', models.IntegerField(default=0)),
                ('Attendance_date10', models.IntegerField(default=0)),
                ('Attendance_date11', models.IntegerField(default=0)),
                ('Attendance_date12', models.IntegerField(default=0)),
                ('Attendance_date13', models.IntegerField(default=0)),
                ('Attendance_date14', models.IntegerField(default=0)),
                ('Attendance_date15', models.IntegerField(default=0)),
                ('Attendance_date16', models.IntegerField(default=0)),
                ('Attendance_date17', models.IntegerField(default=0)),
                ('Attendance_date18', models.IntegerField(default=0)),
                ('Attendance_date19', models.IntegerField(default=0)),
                ('Attendance_date20', models.IntegerField(default=0)),
                ('Attendance_date21', models.IntegerField(default=0)),
                ('Attendance_date22', models.IntegerField(default=0)),
                ('Attendance_date23', models.IntegerField(default=0)),
                ('Attendance_date24', models.IntegerField(default=0)),
                ('Attendance_date25', models.IntegerField(default=0)),
                ('Attendance_date26', models.IntegerField(default=0)),
                ('Attendance_date27', models.IntegerField(default=0)),
                ('Attendance_date28', models.IntegerField(default=0)),
                ('Attendance_date29', models.IntegerField(default=0)),
                ('Attendance_date30', models.IntegerField(default=0)),
                ('Attendance_date31', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'account_attendance_check',
            },
        ),
        migrations.CreateModel(
            name='AccountCherry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cherry', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'account_cherry',
            },
        ),
        migrations.CreateModel(
            name='AccountLoginType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loginType', models.CharField(choices=[('NORMAL', 'Normal'), ('GOOGLE', 'Google')], default='NORMAL', max_length=10)),
            ],
            options={
                'db_table': 'account_login_type',
            },
        ),
        migrations.CreateModel(
            name='AccountPaidMemberType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paidmemberType', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'account_paid_member_type',
            },
        ),
        migrations.CreateModel(
            name='AccountTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ticket', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'account_ticket',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('AttendanceCheck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountattendancecheck')),
                ('Cherry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountcherry')),
                ('loginType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountlogintype')),
                ('paidmemberType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountpaidmembertype')),
                ('Ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.accountticket')),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(default='n', max_length=64)),
                ('nickname', models.CharField(default='n', max_length=64)),
                ('img', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.account')),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]
