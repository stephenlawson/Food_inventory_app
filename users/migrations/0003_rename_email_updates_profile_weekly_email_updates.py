# Generated by Django 4.0.1 on 2022-05-05 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_email_updates'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email_updates',
            new_name='weekly_email_updates',
        ),
    ]
