# Generated by Django 3.2.15 on 2022-09-29 05:40

import auths.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0004_alter_states_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='states',
            name='data',
            field=models.FileField(null=True, upload_to=auths.models.filepath),
        ),
    ]
