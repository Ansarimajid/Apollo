# Generated by Django 3.1 on 2023-08-24 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='subject_expertise',
        ),
        migrations.AddField(
            model_name='staff',
            name='subject_expertise',
            field=models.ManyToManyField(blank=True, to='main_app.Subject'),
        ),
    ]
