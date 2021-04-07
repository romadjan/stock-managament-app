# Generated by Django 3.1.7 on 2021-04-03 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itemstore', '0002_auto_20210403_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='itemstore.category'),
            preserve_default=False,
        ),
    ]