# Generated by Django 5.1.1 on 2024-12-11 03:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemcarrinho',
            name='produto',
        ),
        migrations.AddField(
            model_name='itemcarrinho',
            name='variacao',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.variacaoproduto'),
            preserve_default=False,
        ),
    ]
