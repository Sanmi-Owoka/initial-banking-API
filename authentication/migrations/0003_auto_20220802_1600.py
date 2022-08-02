# Generated by Django 3.2.14 on 2022-08-02 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_passwordresetconfirmation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordresetconfirmation',
            name='number_of_reset',
        ),
        migrations.AddField(
            model_name='passwordresetconfirmation',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.user'),
        ),
    ]
