# Generated by Django 4.2.7 on 2023-12-31 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_book_author'),
        ('transactions', '0002_rename_account_transaction_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance_after_transaction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='book',
            field=models.ManyToManyField(related_name='book_transactions', to='book.book'),
        ),
    ]