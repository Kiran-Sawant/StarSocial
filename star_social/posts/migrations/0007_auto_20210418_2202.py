# Generated by Django 3.1.6 on 2021-04-18 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20210416_2332'),
        ('posts', '0006_auto_20210417_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groupposts', to='groups.group'),
        ),
    ]