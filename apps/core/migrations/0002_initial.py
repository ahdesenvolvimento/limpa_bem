# Generated by Django 3.2 on 2022-04-06 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='atendimento',
            name='id_funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.atendente'),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='id_servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.servico'),
        ),
        migrations.AddField(
            model_name='atendimento',
            name='id_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente'),
        ),
    ]