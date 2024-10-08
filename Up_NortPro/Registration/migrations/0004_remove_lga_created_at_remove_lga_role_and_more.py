# Generated by Django 5.0.7 on 2024-08-02 11:29

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0003_remove_ward_name_ward_fullname_ward_membership_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lga',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='role',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='user',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='national',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='national',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='national',
            name='membership_status',
        ),
        migrations.RemoveField(
            model_name='national',
            name='state',
        ),
        migrations.RemoveField(
            model_name='national',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='national',
            name='user',
        ),
        migrations.RemoveField(
            model_name='national',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='state',
            name='lga',
        ),
        migrations.RemoveField(
            model_name='state',
            name='role',
        ),
        migrations.RemoveField(
            model_name='state',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='state',
            name='user',
        ),
        migrations.RemoveField(
            model_name='state',
            name='ward',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='membership_id',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='role',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='ward',
            name='user',
        ),
        migrations.AddField(
            model_name='lga',
            name='wards',
            field=models.ManyToManyField(to='Registration.ward'),
        ),
        migrations.AddField(
            model_name='national',
            name='states',
            field=models.ManyToManyField(to='Registration.state'),
        ),
        migrations.AddField(
            model_name='state',
            name='lgas',
            field=models.ManyToManyField(to='Registration.lga'),
        ),
        migrations.AddField(
            model_name='ward',
            name='chapter_registered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ward',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lga',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='national',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='state',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='LGAMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('active', 'Active'), ('ward_leader', 'Ward Leader'), ('ward_secretary', 'Ward Secretary'), ('ward_treasurer', 'Ward Treasurer'), ('lga_coordinator', 'LGA Coordinator'), ('lga_secretary', 'LGA Secretary'), ('lga_treasurer', 'LGA Treasurer')], default='active', max_length=20)),
                ('lga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.lga')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lgward', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NationalMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('active', 'Active'), ('ward_leader', 'Ward Leader'), ('ward_secretary', 'Ward Secretary'), ('ward_treasurer', 'Ward Treasurer'), ('lga_coordinator', 'LGA Coordinator'), ('lga_secretary', 'LGA Secretary'), ('lga_treasurer', 'LGA Treasurer'), ('state_coordinator', 'State Coordinator'), ('state_secretary', 'State Secretary'), ('state_treasurer', 'State Treasurer'), ('national_coordinator', 'National Coordinator'), ('national_secretary', 'National Secretary'), ('national_treasurer', 'National Treasurer')], default='active', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='natwards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StateMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('active', 'Active'), ('ward_leader', 'Ward Leader'), ('ward_secretary', 'Ward Secretary'), ('ward_treasurer', 'Ward Treasurer'), ('lga_coordinator', 'LGA Coordinator'), ('lga_secretary', 'LGA Secretary'), ('lga_treasurer', 'LGA Treasurer'), ('state_coordinator', 'State Coordinator'), ('state_secretary', 'State Secretary'), ('state_treasurer', 'State Treasurer')], default='active', max_length=20)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.state')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statewards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WardMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(choices=[('dormant', 'Dormant'), ('active', 'Active'), ('ward_leader', 'Ward Leader'), ('ward_secretary', 'Ward Secretary'), ('ward_treasurer', 'Ward Treasurer')], default='dormant', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ward', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Registration.ward')),
            ],
        ),
        migrations.AddField(
            model_name='ward',
            name='members',
            field=models.ManyToManyField(related_name='myward', through='Registration.WardMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]
