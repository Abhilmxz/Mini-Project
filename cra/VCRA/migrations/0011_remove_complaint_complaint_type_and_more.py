# Generated by Django 5.1.7 on 2025-06-05 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VCRA', '0010_userprofile_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='complaint_type',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='description',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='location',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='proof',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='status',
        ),
    ]
