# Generated by Django 4.2.7 on 2023-12-31 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_borrowbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='BorrowBook',
        ),
    ]
