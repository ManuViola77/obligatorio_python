# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_end', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4, unique=True)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Entrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=11, null=True)),
                ('documento', models.CharField(max_length=11, null=True)),
                ('usada', models.BooleanField(default=False)),
                ('Asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4, unique=True)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100, null=True)),
                ('fecha', models.DateTimeField()),
                ('detalle', models.CharField(max_length=50)),
                ('afiche', models.ImageField(upload_to=b'')),
                ('Categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='PrecioEntrada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('Evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Evento')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=4)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='lugar',
            name='codigo',
            field=models.CharField(max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='direccion',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lugar',
            name='telefono',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='sector',
            name='Lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Lugar'),
        ),
        migrations.AddField(
            model_name='precioentrada',
            name='Sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Sector'),
        ),
        migrations.AddField(
            model_name='evento',
            name='Lugar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Lugar'),
        ),
        migrations.AddField(
            model_name='entrada',
            name='Evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Evento'),
        ),
        migrations.AddField(
            model_name='asiento',
            name='Sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_end.Sector'),
        ),
        migrations.AlterUniqueTogether(
            name='sector',
            unique_together=set([('codigo', 'Lugar')]),
        ),
        migrations.AlterUniqueTogether(
            name='asiento',
            unique_together=set([('numero', 'Sector')]),
        ),
    ]
