# Generated by Django 4.0.4 on 2022-04-14 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_note_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]