# Generated by Django 4.2.6 on 2023-10-08 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_auto_20210619_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_cashier',
            new_name='is_employee',
        ),
    ]