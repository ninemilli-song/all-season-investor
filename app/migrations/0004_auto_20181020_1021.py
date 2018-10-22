# Generated by Django 2.1.2 on 2018-10-20 02:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_asset_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetcategory',
            name='bucket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Bucket'),
        ),
        migrations.AlterField(
            model_name='assettype',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.AssetCategory'),
        ),
    ]
