# Generated by Django 5.1.1 on 2024-12-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_mensagemchat_delete_duvidas'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='feedback_dinamica',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='feedback_entrevista',
            field=models.TextField(blank=True, null=True),
        ),
    ]