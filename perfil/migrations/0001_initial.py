# Generated by Django 5.1.1 on 2024-11-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('curso_ingresso', models.CharField(max_length=100)),
                ('ano_ingresso', models.IntegerField()),
                ('genero', models.CharField(max_length=10)),
                ('data_nascimento', models.DateField()),
                ('telefone_contato', models.CharField(max_length=15)),
                ('feedback_dinamica', models.TextField(blank=True, null=True)),
                ('feedback_entrevista', models.TextField(blank=True, null=True)),
            ],
        ),
    ]